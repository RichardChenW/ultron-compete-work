import axios from 'axios';
import nProgress from 'nprogress';
import 'nprogress/nprogress.css';


// 创建axios实例
const requests = axios.create({
    baseURL: "http://172.18.1.35:8000",
    timeout: 10000,
    // headers: {"User-Agent": "multipart/form-data;charset=utf-8"}
    // headers:{"Authorization":"Bearer token"}
});

// 请求拦截器
requests.interceptors.request.use((config) => {
    nProgress.start();
    return config;
});

// 请求拦截器
requests.interceptors.request.use(
    function (config) {
        nProgress.start();
        return config;
    },
    function (error) {
        nProgress.done();
        return Promise.reject(error);
    });


// 添加响应拦截器
requests.interceptors.response.use(
    function (response) {
        nProgress.done();
        return response;
    }, 
    function (error) {
        nProgress.done();
        return Promise.reject(error);
    });

export default requests;



