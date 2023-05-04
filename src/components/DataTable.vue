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
                    <div v-if="Object.keys(yourRes).length === 0" style="text-align: center;color:#c1c4ce;">No Data Upload</div>
                    <div v-for="(value,key,i) in yourRes" :key="i" class="res-card">
                        <span class="res-key">{{key}} : </span>{{ value }}
                    </div>
                </el-card>
                <el-button icon="el-icon-refresh-right" class="refresh-btn" type="success" @click="refreshData">Refresh Rank</el-button>
            </el-aside>
            <el-main>
                <!-- 表格部分 -->
                <div class="table" >
                    <h5>Rank Table</h5>
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

import "nprogress/nprogress.css";
import nProgress from "nprogress";
import requests from "@/api/request";


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
        async refreshData() {
            let { data: res } = await requests.get("/rank");
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
                this.$message({
                    message: 'please upload file and input your name',
                    type: 'error',
                    showClose: true,
                });
            } else {
                let formData = new FormData();
                formData.append("file", this.fileList[0].raw);
                requests({
                    url: "/upload?operated_by=" + this.formData1.name,
                    method: "post",
                    data: formData,
                    headers: {
                        "Content-Type": "multipart/form-data;charset=utf-8"
                    }
                })
                .then(res => {
                    if (res.status === 200) {
                        this.yourRes = res.data;
                        this.$message({
                            message: 'Upload Success',
                            type: 'success',
                            showClose: true,
                        });
                        this.refreshData();
                    } else {
                        this.$message({
                            message: 'Upload failed',
                            type: 'error',
                            showClose: true,
                        });
                    }
                })
                .catch(err => {
                    console.log(err);
                });
                
            }
        }
    },
    mounted() {
        this.refreshData();
    },
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
    .upload-btn{
        display: flex;
        justify-content: center;
        .el-button--danger{
            margin-top:10px;
            width: 153px;
        }
    }
    .refresh-btn{
        width: 95%;
        margin: 10px;
    }
}
</style>