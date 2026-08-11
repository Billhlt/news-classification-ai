import axios from 'axios'

// 创建axios实例（用于SpringAI，端口8081）
const api = axios.create({
  baseURL: 'http://localhost:8081',
  timeout: 100000, // 100秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 创建FastAPI的axios实例（端口8083）
const fastApi = axios.create({
  baseURL: 'http://localhost:8083',
  timeout: 100000, // 100秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器（SpringAI）
api.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    return config
  },
  (error) => {
    // 对请求错误做些什么
    return Promise.reject(error)
  },
)

// 响应拦截器（SpringAI）
api.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    return response.data
  },
  (error) => {
    // 对响应错误做点什么
    console.error('API Error:', error)
    return Promise.reject(error)
  },
)

// 请求拦截器（FastAPI）
fastApi.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    return config
  },
  (error) => {
    // 对请求错误做些什么
    return Promise.reject(error)
  },
)

// 响应拦截器（FastAPI）
fastApi.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    return response.data
  },
  (error) => {
    // 对响应错误做点什么
    console.error('FastAPI Error:', error)
    return Promise.reject(error)
  },
)

/**
 * 与AI聊天接口
 * @param {string} prompt - 提示词
 * @param {string} chatId - 聊天ID
 * @returns {Promise} 返回AI的回复
 */
export function chatWithAI(prompt, chatId) {
  return api.get('/ai/chat', {
    params: {
      prompt,
      chatId,
    },
  })
}

/**
 * 保存新闻到本地文件（使用FastAPI，端口8083）
 * @param {Array<Array<number, string>>} newsList - 二维列表，格式: [[分类编号, 新闻内容], ...]
 * @returns {Promise} 返回保存结果
 */
export function saveNews(newsList) {
  return fastApi.post('/api/save-news', {
    news_list: newsList,
  })
}

export default {
  chatWithAI,
  saveNews,
}
