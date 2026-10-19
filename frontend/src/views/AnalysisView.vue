<template>
  <div class="analysis-view">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="12">
        <el-card shadow="never" class="analysis-card">
          <template #header>
            <div class="card-header">
              <div class="card-header-left">
                <el-icon :size="18" color="var(--primary)"><DataBoard /></el-icon>
                <span>数据清洗状态</span>
              </div>
              <el-button
                type="primary"
                size="small"
                @click="startClean"
                :disabled="!batchId || cleanStatus === 'processing'"
                :loading="cleanStatus === 'processing'"
              >
                开始清洗
              </el-button>
            </div>
          </template>

          <el-descriptions :column="1" border size="small" v-if="batchInfo">
            <el-descriptions-item label="批次ID">{{ batchInfo.batch_id }}</el-descriptions-item>
            <el-descriptions-item label="文件名">{{ batchInfo.file_name }}</el-descriptions-item>
            <el-descriptions-item label="总记录数">{{ batchInfo.total_count }}</el-descriptions-item>
            <el-descriptions-item label="清洗后数量">{{ batchInfo.clean_count || '-' }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(batchInfo.status)" effect="dark" size="small">
                {{ getStatusText(batchInfo.status) }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>

          <el-empty v-else description="请先上传数据" :image-size="80" />
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12">
        <el-card shadow="never" class="analysis-card">
          <template #header>
            <div class="card-header">
              <div class="card-header-left">
                <el-icon :size="18" color="var(--primary)"><TrendCharts /></el-icon>
                <span>关键词分析</span>
              </div>
              <el-button
                type="primary"
                size="small"
                @click="startAnalysis"
                :disabled="!batchId || cleanStatus !== 'completed' || analysisStatus === 'processing'"
                :loading="analysisStatus === 'processing'"
              >
                开始分析
              </el-button>
            </div>
          </template>

          <el-form label-width="90px" class="analysis-form">
            <el-form-item label="时间维度">
              <el-radio-group v-model="timeDim">
                <el-radio-button label="month">按月</el-radio-button>
                <el-radio-button label="quarter">按季度</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Top N">
              <el-input-number v-model="topN" :min="10" :max="200" :step="10" controls-position="right" />
            </el-form-item>
          </el-form>

          <el-alert
            v-if="analysisStatus === 'processing'"
            title="正在分析中，请稍候..."
            type="info"
            :closable="false"
            show-icon
          />
        </el-card>
      </el-col>
    </el-row>

    <el-card v-if="keywords.length > 0" shadow="never" class="result-card">
      <template #header>
        <div class="card-header">
          <div class="card-header-left">
            <el-icon :size="18" color="var(--primary)"><List /></el-icon>
            <span>Top {{ topN }} 热门技能关键词</span>
          </div>
        </div>
      </template>

      <el-table :data="keywords" border stripe size="small">
        <el-table-column type="index" label="排名" width="70" />
        <el-table-column prop="name" label="技能关键词" />
        <el-table-column prop="value" label="出现次数" width="120" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { DataBoard, TrendCharts, List } from '@element-plus/icons-vue'
import { api } from '@/api/index'

const batchId = ref(localStorage.getItem('batchId') || '')
const batchInfo = ref(null)
const timeDim = ref('month')
const topN = ref(50)
const analysisStatus = ref('')
const keywords = ref([])

const cleanStatus = computed(() => batchInfo.value?.status || '')

const getStatusType = (status) => {
  const types = {
    'uploaded': 'info',
    'processing': 'warning',
    'completed': 'success',
    'analyzed': 'success',
    'failed': 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'uploaded': '已上传',
    'processing': '处理中',
    'completed': '已完成',
    'analyzed': '已分析',
    'failed': '失败'
  }
  return texts[status] || status
}

const fetchBatchInfo = async () => {
  if (!batchId.value) {
    try {
      const res = await api.getLatestBatch()
      if (res.batch_id) {
        batchId.value = res.batch_id
        localStorage.setItem('batchId', res.batch_id)
        batchInfo.value = res
      }
    } catch (error) {
      console.error(error)
    }
    return
  }

  try {
    const res = await api.getCleanStatus(batchId.value)
    batchInfo.value = res
  } catch (error) {
    console.error(error)
  }
}

const startClean = async () => {
  try {
    await api.cleanData(batchId.value)
    ElMessage.success('数据清洗任务已启动')

    const timer = setInterval(async () => {
      await fetchBatchInfo()
      if (cleanStatus.value === 'completed') {
        clearInterval(timer)
        ElMessage.success('数据清洗完成')
      }
    }, 2000)
  } catch (error) {
    ElMessage.error('启动清洗失败')
    console.error(error)
  }
}

const startAnalysis = async () => {
  analysisStatus.value = 'processing'

  try {
    await api.analyzeKeywords(batchId.value, {
      time_dim: timeDim.value,
      top_n: topN.value
    })
    ElMessage.success('关键词分析任务已启动')

    const timer = setInterval(async () => {
      await fetchBatchInfo()
      if (batchInfo.value?.status === 'analyzed') {
        clearInterval(timer)
        analysisStatus.value = 'completed'
        ElMessage.success('关键词分析完成')
        fetchKeywords()
      }
    }, 2000)
  } catch (error) {
    analysisStatus.value = 'failed'
    ElMessage.error('启动分析失败')
    console.error(error)
  }
}

const fetchKeywords = async () => {
  try {
    const res = await api.getKeywords({
      batch_id: batchId.value,
      top_n: 20
    })
    keywords.value = res.keywords
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchBatchInfo()
})
</script>

<style scoped>
.analysis-view {
  max-width: 1400px;
  margin: 0 auto;
}

.analysis-card {
  border-radius: var(--radius-lg);
  border: none;
  height: 100%;
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

.analysis-form {
  padding: 8px 0;
}

.result-card {
  margin-top: 20px;
  border-radius: var(--radius-lg);
  border: none;
}
</style>
