package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

var pt_url = "https://www.pivotaltracker.com/services/v5/projects"

func get(url string, token string) []map[string]interface{} {

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("X-TrackerToken", token)

	c := http.Client{}
	res, _ := c.Do(req)

	body, _ := ioutil.ReadAll(res.Body)

	data := []map[string]interface{}{}
	json.Unmarshal(body, &data)

	return data

}

type info struct {
	name string
	num  int
}

type progress struct {
	id  int
	num int
}

func get_releases(name string,
	proj_id int,
	token string,
	res chan<- info,
	p chan<- progress) {

	offset := 0

	for {

		url := fmt.Sprintf(

			"%v/%v/iterations?scope=current_backlog&offset=%v",
			pt_url,
			proj_id,
			offset)

		data := get(url, token)
		p <- progress{proj_id, offset}

		if len(data) == 0 {
			break
		}

		offset += len(data)

	}

	res <- info{name, offset}

}

func get_progress(pr <-chan progress) {

	for {
		fmt.Println(<-pr)
	}
}

func main() {

	token := os.Args[1]
	data := get(pt_url, token)

	r := make(chan info)
	pr := make(chan progress)

	go get_progress(pr)

	for _, p := range data {

		id := int(p["id"].(float64))
		name := p["name"].(string)

		fmt.Println(
			id,
			name)

		go get_releases(
			name, id, token, r, pr)
	}

        i := []info {}

	for _, _ = range data {
		i = append(i, <-r)
	}

        for _, p := range i {
            fmt.Println(p)
        }

}
