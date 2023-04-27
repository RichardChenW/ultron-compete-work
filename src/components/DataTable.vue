<template>
    <div class="page-container">
        <!-- 标题部分 -->
        <el-header class="header" height="80px">KALIMDOR ULTRON COMPETITION</el-header>
        <!-- 内容部分 -->
        <el-container>
            <!-- 左边栏 -->
            <el-aside width="400px">
                <el-card shadow="hover" class="upload-card">
                    <el-form ref="formData1" :model="formData1">
                        <el-form-item label="Your Name :">
                            <el-input placeholder="Please Input Your Name" v-model="formData1.name"></el-input>
                        </el-form-item>
                            <el-upload 
                                class="upload" 
                                ref="upload" 
                                action="string" 
                                :file-list="fileList"
                                :auto-upload="false" 
                                :on-change="handleChange" 
                                :on-preview="handlePreview"
                                :on-remove="handleRemove" 
                                multiple="multiple"
                            >   
                                <el-button @click="delFile">Select Upload File</el-button>
                            </el-upload>
                    </el-form>
                    <div class="upload-btn">
                        <el-button @click="submitUpload" type="danger">Upload</el-button>
                    </div>
                </el-card>
                <el-card class="box-card" shadow="hover">
                    <div slot="header" class="clearfix">
                        <span>Your Competition Result</span>
                    </div>
                    <div v-for="(value,key,i) in yourRes" :key="i" class="res-card">
                        <span class="res-key">{{key}} : </span>{{ value }}
                    </div>
                </el-card>
                <div class="rank-btn" @click="getData">
                    <div>Click to </div>
                    <div>Check Your Rank</div>
                </div>
                <!-- <button  class="rank-btn"></button> -->
            </el-aside>
            <el-main>
                <!-- 表格部分 -->
                <div class="table" >
                    <el-table  :data="competeData" border style="width: 100%" stripe size="medium">
                        <el-table-column align="center" type="index"></el-table-column>
                        <el-table-column  align="center" prop="name" label="name" >
                        </el-table-column>
                        <el-table-column align="center" prop="operated_at" label="operated_at" >
                        </el-table-column>
                        <el-table-column align="center" prop="auc" label="auc">
                        </el-table-column>
                    </el-table>
                </div>
            </el-main>
            
        </el-container>
    </div>
</template>

<script>
import axios from 'axios'


export default {
    name: "DataTable",
    data() {
        return {
            competeData: [],
            formData1: { name: '' },
            formData: "",
            fileList: [],
            yourRes: {}
        }
    },
    methods: {
        async getData() {
            let { data: res } = await axios.get('http://172.18.1.35:8000/rank');
            this.competeData = res;
        },
        submit() {
            console.log(this.formData.name)
        },

        delFile() {
            this.fileList = [];
        },
        handleChange(file, fileList) {
            this.fileList = fileList;
        },

        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        },
        submitUpload() {
            if (this.formData1.name === "" || this.fileList.length === 0) {
                alert("请输入名称和选取文件");
                return;
            } else {
                let formData = new FormData();
                formData.append("file", this.fileList[0].raw);
                axios({
                    url: "http://172.18.1.35:8000/upload?operated_by=" + this.formData1.name,
                    method: "post",
                    data: formData,
                    headers: {
                        "Content-Type": "multipart/form-data;charset=utf-8"
                    }
                })
                    .then(res => {
                        console.log(res)
                        if (res.status === 200) {
                            this.yourRes = res.data;
                            alert("导入成功!");
                        } else {
                            alert("导入失败!");
                        }
                    })
                    .catch(err => {
                        console.log(err);
                    });
            }
        }
    }

}

</script >

<style lang="scss">
.page-container {
    .header {
        //文字居中
        text-align: center;
        font-size: 30px;
        font-weight: 700;
        line-height: 80px;
        color: #ffffff;
        background-color: #414142;
    }
    .el-table th.el-table__cell {
        color: #414142;
        font-size: 16px;
    }
}

.el-aside {

    height: calc(100vh - 80px);
    display: flex;
    flex-direction: column;
    background-color: #efefef;

    .el-card {
        margin: 10px;

        .el-form-item__label {
            margin-left: 10px;
            font-size: 16px;
            font-weight: 700;
        }

        .el-input__inner {
            margin-left: 10px;
            width: calc(320px) !important;
            &:focus {
                border-color: #000000;
                box-shadow: 0 0 0 1px rgba(0, 0, 0,);
            }
        }
        .el-card__header{
            color: #414142;
            font-weight: 700;
        }
        .upload{
            display: flex;
            flex-direction: row;
            justify-content: center;
            .el-button--default{
                &:hover{
                    // background-color: #000000;
                    color: #000000;
                    // font-weight: 700;
                    border-color:#000000;
                    background-color: #ffffff!important;
                }
                &:focus{
                    color: #000000;
                    border-color:#000000;
                    background-color: #ffffff!important;
                }
            }
        }
    }
    .res-card{
        margin: 10px;
        .res-key{
            font-weight: 700;
        }
    }
    .rank-btn{
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        height: 120px;
        width: 380px;
        margin: 10px;
        font-size: 30px;
        background-color: #ffffff;
        border-radius: 5px;
        border: none;
        &:hover{
            border: 1px solid black;
        }
    }
    .upload-btn{
        display: flex;
        justify-content: center;
        .el-button--danger{
            margin-top:10px;
            width: 153px;
        }
    }
}
</style>