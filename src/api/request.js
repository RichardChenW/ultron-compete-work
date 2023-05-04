import axios from 'axios';
import nProgress from 'nprogress';
import 'nprogress/nprogress.css';


// 创建axios实例
const requests = axios.create({
    baseURL:"http://172.18.1.35:8000",
    timeout: 10000,
});

// 请求拦截器
requests.interceptors.request.use((config)=>{
    nProgress.start();
    return config;
});

// 响应拦截器
requests.interceptors.response.use(
    
    // 成功的回调
    (response)=>{
        nProgress.done();
        return response;
    },
    // 失败的回调
    (error)=>{
        nProgress.done();
        return error; //? 这里返回error会怎么样？
    },
);

export default requests;



