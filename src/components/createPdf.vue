<template>
	<div class="body_main">
		<!-- 滚动条组件包含所有内容 -->
		<vuescroll>
			<el-row style="margin-top:30px;">
				<el-steps :space="300" :active="current" finish-status="success" :align-center="true">
					<el-step :title="item" v-for="item in steps" :key="item"></el-step>
				</el-steps>
			</el-row>
			<el-row>
				<div style="width:90%;height: 450px;background-color: #fff;margin: 20px auto;">
					<div v-show="current==0"  v-loading="loading"
    element-loading-text="数据预处理中，请稍后"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)">
						<div style="padding: 120px 120px 120px 50px;">
							<div>
								<el-button type="primary" @click="getexcel">选择Excel文件</el-button>
								<span style="font-size: 16px;display: block;margin-top: 20px;">{{'Excel路径：'+excel}}</span>
							</div>
							<div style="margin-top: 60px;">
								<div style="margin-bottom: 20px;margin-bottom: 50px;">选择合同模板：</div>
								<el-checkbox-group v-model="checkList" @change="selectcheck" style="margin-left: 30px;">
									<el-checkbox label="G" >{{"广东绿生源合同"}}</el-checkbox>
									<el-checkbox label="Q" >{{"清远酸动力合同"}}</el-checkbox>
									<el-checkbox label="S" >{{"上海酸能埃塞合同"}}</el-checkbox>
								</el-checkbox-group>
							</div>
						</div>
					</div>
					<div v-show="current==1">
						<div style="padding: 100px 0 0 50px;">
							<span>选择字段：</span>
							<el-select v-model="value" placeholder="请选择" @change="selectvalue">
								<el-option v-for="(item,index) in options" :key="index" :label="item" :value="{label: item,index: index+1}">
								</el-option>
							</el-select>
							<span style="margin-left: 20px;">选择分隔符：</span>
							<el-select v-model="divide" placeholder="" @change="selectdivide" style="width: 70px;">
								<el-option v-for="(item,index) in divides" :key="index" :label="item" :value="{label: item,index: index+1}">
								</el-option>
							</el-select>
							<el-button type="primary" style="position: absolute;right: 180px;" @click="addvalue">添加</el-button>
							<div style="margin-top: 40px;">
								{{'文件名：'+rename}}
								<el-button type="primary" style="position: absolute;right: 180px;" @click="deletevalue">删除</el-button>
							</div>
						</div>
					</div>
					<div v-show="current==2">
						<div   v-loading="loadingPrint"
    element-loading-text="程序在运行中，请稍后"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)">
							<el-scrollbar>
								<div style="position: absolute;top: 40px;left: 100px;font-size: 20px;font-weight: 500;">打印日志：</div>
									<div style="padding: 80px 0 0 120px">
										<div style="height:300px;width:80%;overflow:auto;background:#EEEEEE;" class="scrollbars">
											<div v-for="(item,index) in message" :key="index" >
												{{item}}
											</div>
										</div>
									</div>
							</el-scrollbar>
						</div>
					</div>
				</div>
			</el-row>
			<el-row style="display: flex;justify-content: center;padding: 25px;">
				<!-- <el-button v-if="current > 0" style="margin-left: 8px" @click="prev">
					上一步
				</el-button> -->
				<el-button v-if="current==0" type="primary" @click="next" style="margin-left: 20px;">
					下一步
				</el-button>
				<el-button v-if="current==1" type="primary" @click="print" style="margin-left: 20px;">
					开始打印
				</el-button>
				<!-- <el-button v-if="current == steps.length - 1" type="primary" style="margin-left: 20px;" @click="submit">
					完成
				</el-button> -->
				<el-button v-if="current == steps.length - 1" type="warning" style="margin-left: 20px;" @click="stop">
					停止打印
				</el-button>
				<el-button v-if="current == steps.length - 1" type="primary" style="margin-left: 20px;" @click="home">
					返回首页
				</el-button>
			</el-row>
		</vuescroll>
	</div>
</template>

<script>
	// 引入滚动条组件
	import vuescroll from "vuescroll";
	// 引入electron 中的 remote 远程模块
	import {
		remote
	} from "electron";

	export default {
		name: "HomeMain",
		data() {
			return {
				steps: ['步骤一', '步骤二', '步骤三'],
				checkList: [],
				current: 0,
				excel: "", //excel文件路径
				options: ['字段一', '字段二', '字段三', '字段四', '字段五'],
				divides: ['+', '-', '*', '/', '_'],
				value: '',  //选择的字段value
				value_index:'',   //选择的字段index
				divide: '',    //选择的分隔符value
				divide_index:'', //选择的分隔符index
				rename: '',
				renamelist: [],
				pdfpath: "", //pdf文件夹路径
				message: [],
				fieldChoose:[],   //用户选择字段index
				separatorChoose:[],  //用户选择分隔符index
				loading: false,   //加载中标志
				loadingPrint: false,  //打印日志加载
				intervalScroll:null,   //定时下拉滚动条
			};
		},
		components: {
			vuescroll,
		},
		methods: {
			next() {
				this.loading = true
				// this.current++;
				this.stopPrint();
				// this.$axios.post('http://127.0.0.1:8088/getFieldAndSeparator')
				this.$axios.post('http://127.0.0.1:8088/postInformation',{"excel":this.excel,"templateList":this.checkList})
					.then(res=>{
						console.log(res);
						if(res.data.field && res.data.separator){
							this.options= res.data.field
							this.divides = res.data.separator
							this.value = this.options[0]
							this.value_index = 1
							this.divide = this.divides[0]
							this.divide_index = 1

							this.current++;
						}else{
							console.log("解析参数失败")
							this.$message.error("解析参数失败")
						}

						this.loading = false;
					})
					.catch(err=>{
						console.log(err);
						this.loading = false;
						this.$message.error("打开excel 文件出错")

					})
			},
			prev() {
				this.current--;
			},
			print() {

				if(this.rename==''){
					this.$message.warning("请至少选择一个字段！")
					return;
				}
				this.current++;
				this.loadingPrint = true;
				this.$axios.post('http://127.0.0.1:8088/stopPrint')
					.then(res=>{
						console.log(res);
					})
					.catch(err=>{
						console.log(err);
					})
				this.$axios.post('http://127.0.0.1:8088/printContract', {"templateList":this.checkList,"fieldChoose":this.fieldChoose,"separatorChoose":this.separatorChoose})
					.then(res=>{
						console.log(res);
						this.intervalScroll = setInterval(()=>{
							let scrollbar = document.getElementsByClassName("scrollbars")
							// console.log(scrollbar[0].scrollTop+"  " +scroll[0].scrollHeight)
							scrollbar[0].scrollTop=scrollbar[0].scrollHeight
						},1000);
						let interval = setInterval(() => {
							this.$axios.post('http://127.0.01:8088/getLog')
								.then(res=>{
									console.log(res)
									if(res.data.log){
										this.message = this.message.concat(res.data.log)
										let scrollbar = document.getElementsByClassName("scrollbars")
										console.log(scrollbar[0].scrollTop+"  " +scrollbar[0].scrollHeight)
										scrollbar[0].scrollTop=scrollbar[0].scrollHeight
										console.log(res);
										this.loadingPrint = false;
									}else{
										console.log("请求数据没有log")
										if(res.data!="暂时没有数据"){

											if(res.data=="程序已结束"){
												this.message = this.message.concat("##################### 程序已结束 #####################")
												let scrollbar = document.getElementsByClassName("scrollbars")
												console.log(scrollbar)
												console.log(scrollbar[0].scrollTop+"  " +scrollbar[0].scrollHeight)
												scrollbar[0].scrollTop=scrollbar[0].scrollHeight
												console.log(scrollbar)
											}

											clearInterval(interval)
											clearInterval(this.intervalScroll)
											this.loadingPrint = false;
											// this.message = this.message.concat("#####################    程序已结束    #####################")
										}
										
									}
								}).catch(err=>{
									console.log(err)
									this.loadingPrint = false;
									this.$message.error("请求日志数据出错")
									console.log("请求日志数据出错")
									this.stopPrint()
									this.message = this.message.concat("#####################    程序已结束    #####################")
									clearInterval(interval)
									clearInterval(this.intervalScroll)
								})
						}, 5000);
					})
					.catch(err=>{
						console.log(err);
						this.loadingPrint = false;
						this.$message.error("打印合同单出错")
					})
			},
			submit() {
				this.current++;
				this.$message.success('打印PDF成功！')
				this.$router.push('/');
			},
			home(){
				this.$confirm('此操作将返回首页, 如果程序未终止，将终止程序，是否继续?', '提示', {
									confirmButtonText: '确定',
									cancelButtonText: '取消',
									type: 'warning'
									}).then(() => {
										this.stopPrint();
										this.$router.push('/');
									}).catch(() => {
										this.$message({
											type: 'info',
											message: '已取消'
										});          
								});
			},
			stopPrint(){
				this.$axios.post('http://127.0.0.1:8088/stopPrint')
					.then(res=>{
						console.log(res);
					})
					.catch(err=>{
						console.log(err);
					})
			},
			stop(){
				this.$confirm('此操作将停止程序运行, 是否继续?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
					}).then(() => {
					this.$message({
						type: 'success',
						message: '停止成功!'
					});
					this.stopPrint();
					}).catch(() => {
					this.$message({
						type: 'info',
						message: '已取消'
					});          
				});
			},
			selectcheck(e) {
				console.log(e);
				// this.$axios.post('http://127.0.0.1:8088/postTemplate', {"templateList":this.checkList})
				// 	.then(res=>{
				// 		console.log(res);
				// 	})
				// 	.catch(err=>{
				// 		console.log(err);
				// 	})
			},
			selectvalue(e) {
				this.value = e.label;
				this.value_index = e.index
				console.log(e);

			},
			selectdivide(e) {
				this.divide = e.label;
				this.divide_index = e.index
				console.log(e);
			},
			addvalue() {
				console.log(this.value)
				//插入用户选择的字段
				console.log(this.fieldChoose)
				if(this.fieldChoose.length ==0){
					console.log(this.value)
					this.fieldChoose.push(this.value_index)
				}else{
					this.separatorChoose.push(this.divide_index)
					this.fieldChoose.push(this.value_index)
				}

				console.log(this.fieldChoose,"  +++   ",this.separatorChoose)
				if (this.rename == '') {
					this.renamelist.push(this.value);
					this.rename = this.renamelist[0];
				} else {
					this.renamelist.push(this.divide);
					this.renamelist.push(this.value);
					this.rename = '';
					for (let i = 0; i < this.renamelist.length; i++) {
						this.rename = this.rename + this.renamelist[i];
					}
				}
			},
			deletevalue() {
				//弹出用户选择的字段
				this.fieldChoose.pop()
				this.separatorChoose.pop()

				this.renamelist.pop();
				this.renamelist.pop();
				this.rename = '';
				for (let i = 0; i < this.renamelist.length; i++) {
					this.rename = this.rename + this.renamelist[i];
				}
			},
			// 获取pdf文件夹路径
			getpdfpath() {
				let path = remote.dialog.showOpenDialog({
					title: "选择pdf文件路径",
					properties: ["openDirectory"],
				});
				this.pdfpath = path[0];
				console.log(this.pdfpath);
			},
			// 获取excel文件路径
			getexcel() {
				let path = remote.dialog.showOpenDialog({
					title: "选择Excel文件",
					properties: ["openFile"],
				});
				this.excel = path[0];
				// this.stopPrint();
				// this.$axios.post('http://127.0.0.1:8088/postPath', {"excel":this.excel})
				// 	.then(res=>{
				// 		console.log(res);
				// 	})
				// 	.catch(err=>{
				// 		console.log(err);
				// 	})
				// console.log(this.excel);
			},
		},
	};
</script>

<style scoped>
	.body_main {
		width: 100%;
		background-color: var(--color-boby-main-bg);
		height: 100%;
		border-radius: 7px;
		overflow-x: hidden;
	}
</style>
