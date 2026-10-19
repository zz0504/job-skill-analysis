<template>
  <div class="data-view">
    <el-card class="upload-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="card-header-left">
            <el-icon :size="18" color="var(--primary)"><Upload /></el-icon>
            <span>数据上传</span>
          </div>
        </div>
      </template>

      <div class="upload-area">
        <el-upload
          ref="uploadRef"
          :http-request="handleUploadRequest"
          :on-success="handleSuccess"
          :on-error="handleError"
          :before-upload="beforeUpload"
          :limit="1"
          :auto-upload="true"
          accept=".csv,.xlsx,.xls"
          class="custom-upload"
        >
          <div class="upload-placeholder">
            <el-icon :size="32" color="#c0c4cc"><Plus /></el-icon>
            <p class="upload-text">点击或拖拽文件到此区域上传</p>
            <p class="upload-hint">支持 CSV、Excel 格式，文件大小不超过 50MB</p>
          </div>
        </el-upload>
      </div>

      <div class="test-data-section">
        <el-divider>
          <span class="divider-text">或使用测试数据</span>
        </el-divider>
        <el-button
          type="success"
          size="large"
          :loading="testLoading"
          class="test-data-btn"
          @click="handleLoadTestData"
        >
          <el-icon style="margin-right: 6px;"><Document /></el-icon>
          加载测试数据（500条招聘岗位）
        </el-button>
      </div>
    </el-card>

    <el-card v-if="batchId" class="preview-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="card-header-left">
            <el-icon :size="18" color="var(--primary)"><List /></el-icon>
            <span>数据预览</span>
          </div>
          <el-tag type="primary" effect="plain">共 {{ pagination.total }} 条数据</el-tag>
        </div>
      </template>

      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
        style="width: 100%"
        size="small"
      >
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="job_title" label="岗位名称" min-width="150" />
        <el-table-column prop="company" label="公司" min-width="150" />
        <el-table-column prop="publish_date" label="发布时间" width="120">
          <template #default="{ row }">
            {{ formatDate(row.publish_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="技能描述" min-width="200" show-overflow-tooltip />
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchData"
        @current-change="fetchData"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Plus, List, Document } from '@element-plus/icons-vue'
import { api } from '@/api/index'
import dayjs from 'dayjs'

const batchId = ref(null)
const loading = ref(false)
const testLoading = ref(false)
const tableData = ref([])
const uploadRef = ref(null)

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const beforeUpload = (file) => {
  const isLt50M = file.size / 1024 / 1024 < 50
  if (!isLt50M) {
    ElMessage.error('文件大小不能超过 50MB!')
    return false
  }
  return true
}

const handleUploadRequest = async (options) => {
  const { file, onSuccess, onError } = options
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await api.upload(formData)
    onSuccess(response)
  } catch (error) {
    onError(error)
  }
}

const handleSuccess = (response) => {
  ElMessage.success(`上传成功！共 ${response.total_count} 条数据`)
  batchId.value = response.batch_id
  localStorage.setItem('batchId', response.batch_id)
  fetchData()
}

const handleError = (error) => {
  const message =
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    error?.message ||
    '上传失败，请重试'
  ElMessage.error(message)
  console.error(error)
}

const handleLoadTestData = async () => {
  testLoading.value = true
  try {
    const response = await api.loadTestData()
    ElMessage.success(`测试数据加载成功！共 ${response.total_count} 条数据`)
    batchId.value = response.batch_id
    localStorage.setItem('batchId', response.batch_id)
    fetchData()
  } catch (error) {
    const message =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.message ||
      '测试数据加载失败，请重试'
    ElMessage.error(message)
    console.error(error)
  } finally {
    testLoading.value = false
  }
}

const fetchData = async () => {
  if (!batchId.value) return

  loading.value = true
  try {
    const res = await api.getJobs({
      batch_id: batchId.value,
      page: pagination.page,
      page_size: pagination.pageSize
    })

    tableData.value = res.data
    pagination.total = res.total
  } catch (error) {
    ElMessage.error('获取数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  return date ? dayjs(date).format('YYYY-MM-DD') : '-'
}
</script>

<style scoped>
.data-view {
  max-width: 1400px;
  margin: 0 auto;
}

.upload-card {
  border-radius: var(--radius-lg);
  border: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 15px;
}

.upload-area {
  padding: 8px 0;
}

.custom-upload :deep(.el-upload) {
  width: 100%;
}

.upload-placeholder {
  border: 2px dashed #d9d9d9;
  border-radius: var(--radius-lg);
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: #fafafa;
}

.upload-placeholder:hover {
  border-color: var(--primary);
  background: #f0f7ff;
}

.upload-text {
  margin: 12px 0 6px;
  font-size: 15px;
  color: var(--text-secondary);
}

.upload-hint {
  margin: 0;
  font-size: 12px;
  color: var(--text-light);
}

.preview-card {
  margin-top: 20px;
  border-radius: var(--radius-lg);
  border: none;
}

.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}

.test-data-section {
  margin-top: 20px;
}

.divider-text {
  font-size: 13px;
  color: var(--text-light);
}

.test-data-btn {
  width: 100%;
  height: 44px;
  font-size: 15px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  border: none;
  transition: all 0.3s;
}

.test-data-btn:hover {
  background: linear-gradient(135deg, #85ce61 0%, #a3d977 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.4);
}
</style>
