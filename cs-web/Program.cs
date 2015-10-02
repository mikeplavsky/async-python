using System;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace TestPivotal
{
    class Progress
    {
        public dynamic Project { get; set; }
        public long Offset { get; set; }
    }

    class Program
    {
        private static string Url = "https://www.pivotaltracker.com/services/v5/projects";

        static dynamic[] GetObjects(string url, string token)
        {
            var client = new WebClient();
            client.Headers.Set("X-TrackerToken", token);
            return JsonConvert.DeserializeObject<dynamic[]>(client.DownloadString(url));
        }

        static void GetIterations(dynamic project, string token, BlockingCollection<Progress> progress)
        {
            long offset = 0;
            while (true)
            {
                var url = Url + string.Format(@"/{0}/iterations?scope=current_backlog&offset={1}", project.id, offset);
                var items = GetObjects(url, token);
                if (items.Length == 0)
                    break;

                progress.Add(new Progress{ Project = project, Offset = offset += items.Length });
            }
        }

        static void Progress(BlockingCollection<Progress> queue)
        {
            while (true)
            {
                var item = queue.Take();
                Console.WriteLine(item.Project.name + " " + item.Offset);                   
            }
        }

        static void Run(string token)
        {
            var projects = GetObjects(Url, token);
            var queue = new BlockingCollection<Progress>(new ConcurrentQueue<Progress>());

            new Thread(() => Progress(queue)).Start();
            Parallel.For(0, projects.Count(), i => GetIterations(projects[i], token, queue));
        }

        static void Main(string[] args)
        {
            var sw = Stopwatch.StartNew();

            Run(args[0]);

            sw.Stop();
            Console.WriteLine("Total time {0}", sw.Elapsed.TotalSeconds);
        }
    }
}

