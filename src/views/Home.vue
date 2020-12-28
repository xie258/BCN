<template>
	<!-- 整个框 -->
	<div class="div">
		<!-- 导航栏区域块 -->
		<el-row style="-webkit-app-region: drag" class="category">
			<el-col :span="24">
				<div>
					<!-- 左边ico图案 -->
					<i class="el-icon-my-piliang2 piliangcaozuo"></i>
					<span class="BO"> BO </span>
					<i class="el-icon-s-home home ihover" @click="home"></i>
					<!-- <i class="el-icon-back back ihover"></i>
					<i class="el-icon-right forward ihover"></i> -->
					<!-- 右边ico图案 -->
					<i class="el-icon-my-weiyi weiyi ihover"></i>
					<i class="el-icon-message message ihover"></i>
					<i class="el-icon-setting setting ihover" @click="message"></i>
					<span class="l"> | </span>
					<i class="el-icon-minus minus ihover" @click="minimizeWin"></i>
					<i class="el-icon-plus plus ihover" @click="maximizeWin"></i>
					<i class="el-icon-close close ihover" @click="closeWin"></i>
				</div>
			</el-col>
		</el-row>

		<!--内容块 -->
		<div class="div_body">
			<!-- 内容快左侧 -->
			<div class="div_body_left">
				<el-menu :router="true">
					<el-menu-item index="/createPdf">
						<span slot="title">批量生成PDF文件</span>
					</el-menu-item>
					<el-menu-item index="/rename">
						<span slot="title">批量改合同名</span>
					</el-menu-item>
					<el-menu-item index="/sendemail">
						<span slot="title">批量发送邮件</span>
					</el-menu-item>
					<el-menu-item index="/any">
						<span slot="title">其他</span>
					</el-menu-item>
				</el-menu>
			</div>
			<!-- 内容快右侧主体部分 -->
			<div class="div_body_main">
				<router-view></router-view>
				<!-- <HomeMain></HomeMain> -->
			</div>
		</div>
	</div>
</template>

<script>
	// @ is an alias to /src
	// import HelloWorld from '@/components/HelloWorld.vue'
	import {
		remote
	} from "electron";
	// import HomeMain from "../components/HomeMain.vue";
	// import {
	// 	ipcRenderer
	// } from "electron";
	// import HomeFooter from '../components/HomeFooter.vue'

	export default {
		name: "Home",
		data() {
			return {
				tabPosition: "left", //内容块左侧 选项卡所在位置
				excelpath: "", //excel文件路径
			};
		},
		components: {
			// HomeMain,
			// HomeFooter
		},
		methods: {
			minimizeWin() {
				remote.getCurrentWindow().minimize(); // 窗口最小化
			},
			home() {
				this.stopPrint();
				this.$router.push('/');
			},
			maximizeWin() {
				const win = remote.getCurrentWindow();
				if (win.isMaximized()) {
					// 判断 窗口是否已最大化
					win.restore(); // 恢复原窗口大小
				} else {
					win.maximize(); //最大化窗口
				}
			},
			closeWin() {
				this.stop();
				// remote.getCurrentWindow().close(); // 关闭窗口，也结束了所有进程
			},
			message() {
				// ipcRenderer.send("message", "我是渲染进程发送给主进程的数据");
			},
			stop(){
				this.$confirm('此操作将退出软件, 是否继续?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
					}).then(() => {

					this.stopPrint();
					this.kill();
					}).catch(() => {
					this.$message({
						type: 'info',
						message: '已取消'
					});          
				});
			},
			kill(){
					this.$axios.post('http://127.0.0.1:8088/kill')
					.then(res=>{
						console.log(res);
						remote.getCurrentWindow().close(); // 关闭窗口，也结束了所有进程
					})
					.catch(err=>{
						console.log(err);
						this.$message.warning("程序运行错误，关闭失败")
						remote.getCurrentWindow().close(); // 关闭窗口，也结束了所有进程
					})
					
			},
			stopPrint(){
				this.$axios.post('http://127.0.0.1:8088/stopPrint')
					.then(res=>{
						console.log(res);
						// this.kill();
						// remote.getCurrentWindow().close(); // 关闭窗口，也结束了所有进程
					})
					.catch(err=>{
						console.log(err);
						// this.kill();
						this.$message.warning("程序运行错误")
						// remote.getCurrentWindow().close(); // 关闭窗口，也结束了所有进程
					})
			},
		},
	};
</script>

<style scoped>
	.div {
		height: 100%;
	}

	.div_body {
		background-color: var(--color-bg);
		/* width: 100%; */
		height: 100%;
	}

	.div_body_left {
		float: left;
		height: 100%;
		width: 20%;
	}

	.div_body_main {
		float: left;
		width: 80%;
	}

	.category {
		margin: 0;
		padding: 0;
		height: var(--height-category);
		z-index: 100;
		background: var(--color-category-bg);
	}

	.BO {
		position: var(--el-ico-position);
		top: calc(var(--el-ico-top) * 0.7);
		color: var(--color-theme);
		font-size: calc(var(--el-ico-font-size) * 1.3);
		left: 67px;
	}

	.ihover:hover {
		color: var(--el-ico-color-hover);
		font-size: calc(var(--el-ico-font-size) * 1.1);
	}

	.weiyi:hover {
		color: var(--color-weiyi-hover);
		font-size: calc(var(--el-ico-font-size) * 1.25);
	}

	.piliangcaozuo {
		position: var(--el-ico-position);
		top: calc(var(--el-ico-top) * 0.5);
		color: var(--color-theme);
		font-size: calc(var(--el-ico-font-size) * 2);
		left: 25px;
	}

	.home {
		position: var(--el-ico-position);
		top: var(--el-ico-top);
		color: var(--el-ico-color);
		font-size: calc(var(--el-ico-font-size) * 1.1);
		-webkit-app-region: var(--no-drag);
		left: 140px;
	}

	.back {
		position: var(--el-ico-position);
		top: calc(var(--el-ico-top) * 1.1);
		color: var(--el-ico-color);
		font-size: var(--el-ico-font-size);
		-webkit-app-region: var(--no-drag);
		left: 185px;
	}

	.forward {
		position: var(--el-ico-position);
		top: calc(var(--el-ico-top) * 1.1);
		color: var(--el-ico-color);
		font-size: var(--el-ico-font-size);
		-webkit-app-region: var(--no-drag);
		left: 210px;
	}

	.weiyi {
		position: var(--el-ico-position);
		top: var(--el-ico-top);
		color: rgb(153, 62, 214);
		font-size: calc(var(--el-ico-font-size) * 1.1);
		-webkit-app-region: var(--no-drag);
		right: 250px;
	}

	.message {
		position: var(--el-ico-position);
		top: var(--el-ico-top);
		color: var(--el-ico-color);
		font-size: var(--el-ico-font-size);
		-webkit-app-region: var(--no-drag);
		right: 200px;
	}

	.setting {
		position: var(--el-ico-position);
		top: var(--el-ico-top);
		color: var(--el-ico-color);
		font-size: var(--el-ico-font-size);
		-webkit-app-region: var(--no-drag);
		right: 165px;
	}

	.l {
		position: var(--el-ico-position);
		top: calc(var(--el-ico-top) * 0.6);
		color: rgb(194, 178, 178);
		font-size: calc(var(--el-ico-font-size) * 1.1);
		right: 127px;
	}

	.minus {
		position: var(--el-ico-position);
		top: var(--el-ico-top);
		color: var(--el-ico-color);
		font-size: var(--el-ico-font-size);
		-webkit-app-region: var(--no-drag);
		right: 73px;
	}

	.plus {
		position: var(--el-ico-position);
		top: var(--el-ico-top);
		color: var(--el-ico-color);
		font-size: var(--el-ico-font-size);
		-webkit-app-region: var(--no-drag);
		right: 45px;
	}

	.close {
		position: var(--el-ico-position);
		top: var(--el-ico-top);
		color: var(--el-ico-color);
		font-size: var(--el-ico-font-size);
		-webkit-app-region: var(--no-drag);
		right: 17px;
	}
</style>
