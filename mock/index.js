import Mock from "mockjs";


Mock.mock("http://172.18.1.6:8000/rank","get",Mock.mock({

"array|10":[
        {
            "name":"@name",
            "operated_at":"@date",
            "auc":"@float(0, 1, 2)"
        }
    ]
}))
