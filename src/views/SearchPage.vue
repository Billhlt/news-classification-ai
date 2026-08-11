<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const searchQuery = ref('')
const searchInput = ref<HTMLTextAreaElement | null>(null)
const router = useRouter()

const adjustTextareaHeight = () => {
  if (searchInput.value) {
    // 重置高度以获取正确的scrollHeight
    searchInput.value.style.height = 'auto'
    // 设置新高度，但不超过最大高度
    const newHeight = Math.min(searchInput.value.scrollHeight, 120)
    searchInput.value.style.height = `${newHeight}px`
  }
}

const handleSearch = () => {
  // 检查搜索查询值是否为非空字符串（去除首尾空格后）
  if (searchQuery.value.trim()) {
    // 处理文本：将连续的换行符替换为单个换行符
    let processedContent = searchQuery.value.replace(/\n+/g, '\n')
    // 清除末尾的所有空格和换行符
    processedContent = processedContent.trimEnd()
    // 跳转到文本框页面
    router.push({
      path: '/textbox',
      query: { content: processedContent },
    })
  }
}

// 监听输入变化，自动调整高度
const handleInput = () => {
  nextTick(() => {
    adjustTextareaHeight()
  })
}

// 组件挂载后初始化高度
onMounted(() => {
  nextTick(() => {
    adjustTextareaHeight()
  })
})
</script>

<template>
  <div class="search-container">
    <div class="logo">
      <h1>新闻整理</h1>
    </div>
    <div class="search-box">
      <textarea
        ref="searchInput"
        v-model="searchQuery"
        class="search-input"
        placeholder="请输入搜索内容"
        rows="1"
        @input="handleInput"
        @keydown.enter.shift.exact.prevent="handleSearch"
        @keydown.enter.ctrl.exact.prevent="handleSearch"
      ></textarea>
      <button class="search-button" @click="handleSearch">发送</button>
    </div>
  </div>
</template>

<style scoped>
.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
  position: relative;
}

.logo {
  position: absolute;
  top: 30vh;
  left: 50%;
  transform: translateX(-50%);
}

.logo h1 {
  font-size: 60px;
  color: #4e6ef2;
  font-weight: normal;
  margin: 0;
}

.search-box {
  display: flex;
  width: 640px;
  align-items: flex-start;
  margin-top: 80px;
}

.search-input {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #4e6ef2;
  border-radius: 10px 0 0 10px;
  outline: none;
  box-sizing: border-box;
  resize: none;
  overflow-y: auto;
  white-space: pre-wrap;
  line-height: 1.5;
}

.search-input:focus {
  border-color: #4662d9;
}

.search-button {
  width: 108px;
  min-height: 44px;
  background-color: #4e6ef2;
  color: white;
  font-size: 17px;
  border: none;
  border-radius: 0 10px 10px 0;
  cursor: pointer;
  outline: none;
  align-self: stretch;
}

.search-button:hover {
  background-color: #4662d9;
}

@media (max-width: 768px) {
  .search-box {
    width: 90%;
  }
}
</style>
