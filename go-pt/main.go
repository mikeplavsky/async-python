package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

var pt_url = "https://www.pivotaltracker.com/services/v5/projects"

func main() {

	token := os.Args[1]

	req, _ := http.NewRequest("GET", pt_url, nil)
	req.Header.Set("X-TrackerToken", token)

	c := http.Client{}
	res, _ := c.Do(req)

	body, _ := ioutil.ReadAll(res.Body)

	data := []map[string]interface{}{}
	json.Unmarshal(body, &data)

	for _, p := range data {

		id := int(p["id"].(float64))

		fmt.Println(
			id,
			p["name"])
	}

}
