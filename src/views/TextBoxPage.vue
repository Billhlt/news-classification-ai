<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { chatWithAI, saveNews } from '../api/api'
import { prompts } from '../utils/prompts'

const route = useRoute()
const router = useRouter()
const leftContent = ref('')
const rightContent = ref('')
const newsList = ref<string[]>([]) // 存储原始新闻内容
const analysisList = ref<string[]>([]) // 存储AI分析结果
const TDList01 = ref<number[][]>([]) // 由analysisList列表转换而成的第一个二维列表
const finallist = ref<[number, string][]>([])
// 获取从SearchPage传递过来的内容
onMounted(() => {
  if (route.query.content) {
    leftContent.value = route.query.content as string
  }
})
//项目总体逻辑:
// 返回到SearchPage
const goBackToSearch = () => {
  router.push('/')
}

// 处理开始按钮点击事件
const handleStart = async () => {
  // 将leftContent.value的内容按换行符分割
  const lines = leftContent.value.split('\n')

  // 将分割后的内容存入newsList，同时初始化analysisList
  newsList.value = lines
  analysisList.value = new Array(lines.length).fill('')

  // 在right-box中显示步骤完成信息
  rightContent.value = '步骤一：存入列表-->完成'

  // 使用CategoryAnalysis提示词分析每个新闻条目
  await processNewsWithAI()

  // 将leftContent内容转换为多个长条形div
  transformToNewsBars()

  console.log('newsList:', newsList.value)
  console.log('analysisList:', analysisList.value)
}

// 使用AI处理新闻列表
const processNewsWithAI = async () => {
  rightContent.value = '步骤二：开始使用AI分析新闻内容...'

  try {
    // 遍历列表中的每个新闻条目
    // 1. 先构造出所有 Promise
    const tasks = newsList.value.map((news, i) =>
      chatWithAI(`${prompts.CategoryAnalysis}\n\n新闻内容：${news ?? ''}`, `news_analysis_${i}`),
    )
    // 2. 并发执行，全部完成后再一次性写回
    const results = await Promise.all(tasks)
    results.forEach((res, i) => (analysisList.value[i] = res))

    rightContent.value = '步骤二：AI分析完成'
  } catch (error) {
    console.error('处理新闻时出错:', error)
    const errorMessage = error instanceof Error ? error.message : String(error)
    rightContent.value = `处理新闻时出错: ${errorMessage}`
  }
}

// 将leftContent内容转换为多个长条形div
const transformToNewsBars = () => {
  let htmlContent = ''

  // 为每个新闻创建一个长条形div
  newsList.value.forEach((news, index) => {
    htmlContent += `
      <div class="news-bar" data-index="${index}">
        <span class="news-number">${analysisList.value[index]}</span>
        <span class="news-content">${news}</span>

      </div>
    `
  })

  // 将生成的HTML内容放入leftContent变量中
  leftContent.value = htmlContent
}

const sort = async () => {
  // 重排新闻条目
  const intList = analysisList.value.map(Number) // 将analysisList列表转换为数字列表
  let index = 1
  for (const value of intList) {
    //生成第一个二维列表
    if (value !== undefined) {
      TDList01.value.push([index, value])
      index++
    } else {
      console.error(`sortandwrite 错误: 第 ${index} 项的 value 为 undefined`)
      rightContent.value = `错误：第 ${index} 项的分析结果为 undefined，请检查AI返回结果或数据格式是否正确。`
    }
  }
  // 异步执行排序操作，避免阻塞UI
  const TDList02 = await new Promise<typeof TDList01.value>((resolve) => {
    setTimeout(() => {
      const sorted = TDList01.value.slice().sort((x, y) => x[1]! - y[1]!) // 对第一个二维列表进行排序，排序为按照每个列表元素的第二个number类型元素的递增顺序进行排序
      resolve(sorted)
    }, 0)
  })
  let htmlContent = ''
  for (let i = 0; i < TDList02.length; i++) {
    htmlContent += `
      <div class="news-bar" data-index="${i}">
        <span class="news-number">${TDList02[i]![1]}</span>
        <span class="news-content">${newsList.value[TDList02[i]![0]! - 1]}</span>

      </div>
    `
    finallist.value.push([TDList02[i]![1]!, newsList.value[TDList02[i]![0]! - 1]!]) // 将排序后的新闻条目存入finallist列表
    // 为每个列表元素的第二个string类型数据的最前面补充"- "
    finallist.value[finallist.value.length - 1]![1] =
      `- ${finallist.value[finallist.value.length - 1]![1]}`
  }

  // 将生成的HTML内容放入leftContent变量中
  leftContent.value = htmlContent
  console.log('intList:', intList)
  console.log('TDList01:', TDList01.value)
  console.log('TDList02:', TDList02)
  rightContent.value = '步骤三：重排完成'
}

const append = async () => {
  saveNews(finallist.value)
  console.log('finallist:', finallist.value)
  rightContent.value = '步骤四：已保存到本地文件'
}
</script>

<template>
  <div class="textbox-container">
    <button class="back-button" @click="goBackToSearch">返回</button>
    <button class="start-button" @click="handleStart">开始</button>
    <button class="sort-button" @click="sort">重排</button>
    <button class="append-button" @click="append">追加</button>
    <!--<button class="test-ai-button-01" @click="testAI">测试AI</button>-->
    <div class="left-box">
      <div v-if="newsList.length > 0" v-html="leftContent" class="news-container"></div>
      <textarea v-else v-model="leftContent" readonly></textarea>
    </div>
    <div class="right-box">
      <textarea v-model="rightContent"></textarea>
    </div>
  </div>
</template>

<style scoped>
.textbox-container {
  position: relative;
  display: flex;
  height: 100vh;
  padding: 20px;
  gap: 20px;
  box-sizing: border-box;
  background-color: #f5f5f5;
}

.left-box,
.right-box {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 20px;
  overflow-y: auto;
}

.news-container {
  width: 90%;
  height: 90%;
  padding: 20px;
  border: 2px solid #4e6ef2;
  border-radius: 10px;
  background-color: white;
  overflow-y: auto;
  box-sizing: border-box;
}

textarea {
  width: 90%;
  height: 90%;
  padding: 20px;
  font-size: 16px;
  line-height: 1.5;
  border: 2px solid #4e6ef2;
  border-radius: 10px;
  outline: none;
  box-sizing: border-box;
  resize: none;
  background-color: white;
}

textarea:focus {
  border-color: #4662d9;
}

textarea[readonly] {
  background-color: #f9f9f9;
  cursor: not-allowed;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 8px 16px;
  background-color: #4e6ef2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  z-index: 10;
}

.back-button:hover {
  background-color: #4662d9;
}

.start-button {
  position: absolute;
  top: 60px;
  left: 20px;
  padding: 8px 16px;
  background-color: #4e6ef2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  z-index: 10;
}

.start-button:hover {
  background-color: #4662d9;
}

.sort-button {
  position: absolute;
  top: 100px;
  left: 20px;
  padding: 8px 16px;
  background-color: #4e6ef2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  z-index: 10;
}

.sort-button:hover {
  background-color: #4662d9;
}
.append-button {
  position: absolute;
  top: 140px;
  left: 20px;
  padding: 8px 16px;
  background-color: #4e6ef2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  z-index: 10;
}

.append-button:hover {
  background-color: #4662d9;
}

.test-ai-button-01 {
  position: absolute;
  top: 60px;
  right: 20px;
  padding: 8px 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  z-index: 10;
}

.test-ai-button-01:hover {
  background-color: #218838;
}

/* 1. 让新闻条目变成 flex 横向排列 */
.news-bar {
  display: flex; /* 关键：横向排列 */
  align-items: flex-start; /* 顶部对齐 */
  margin-bottom: 15px;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}

.news-bar:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 2. 数字小方块：去掉原来的 margin-bottom，让它成为独立列 */
.news-number {
  flex-shrink: 0; /* 防止被挤压 */
  width: 24px;
  height: 24px;
  margin-right: 12px; /* 与文字隔开 */
  background: #409eff;
  color: #fff;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

/* 3. 文字区域：占满剩余宽度 */
.news-content {
  flex: 1;
  font-size: 16px;
  line-height: 1.5;
  color: #333;
}
</style>
