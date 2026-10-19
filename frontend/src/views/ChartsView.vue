<template>
  <div class="charts-view">
    <el-card v-if="keywords.length" shadow="never" class="chart-card full-width">
      <template #header>
        <div class="card-header">
          <div class="card-header-left">
            <el-icon :size="18" color="var(--primary)"><Cloudy /></el-icon>
            <span>热门技能词云</span>
          </div>
        </div>
      </template>
      <WordCloudChart
        :data="keywords"
        height="500px"
      />
    </el-card>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :xs="24" :md="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <div class="card-header-left">
                <el-icon :size="18" color="var(--primary)"><TrendCharts /></el-icon>
                <span>技能趋势变化</span>
              </div>
            </div>
          </template>
          <LineChart
            :data="trendData"
            title="技能趋势变化"
            height="400px"
          />
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <div class="card-header-left">
                <el-icon :size="18" color="var(--primary)"><Histogram /></el-icon>
                <span>岗位技能分布</span>
              </div>
            </div>
          </template>
          <BarChart
            :data="categoryData"
            title="岗位技能分布"
            height="400px"
          />
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="!keywords.length" description="暂无图表数据，请先进行关键词分析" :image-size="100" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Cloudy, TrendCharts, Histogram } from '@element-plus/icons-vue'
import { api } from '@/api/index'
import WordCloudChart from '@/components/charts/WordCloudChart.vue'
import LineChart from '@/components/charts/LineChart.vue'
import BarChart from '@/components/charts/BarChart.vue'

const batchId = ref(localStorage.getItem('batchId') || '')
const keywords = ref([])
const trendData = ref({})
const categoryData = ref({})

const fetchLatestBatch = async () => {
  try {
    const res = await api.getLatestBatch()
    if (res.batch_id) {
      batchId.value = res.batch_id
      localStorage.setItem('batchId', res.batch_id)
    }
  } catch (error) {
    console.error(error)
  }
}

const fetchKeywords = async () => {
  if (!batchId.value) {
    await fetchLatestBatch()
  }
  
  if (!batchId.value) return

  try {
    const res = await api.getKeywords({
      batch_id: batchId.value,
      top_n: 30
    })
    keywords.value = res.keywords
  } catch (error) {
    console.error(error)
  }
}

const fetchTrendData = async () => {
  if (!batchId.value) return

  try {
    const topKeywords = keywords.value.slice(0, 5).map(k => k.name).join(',')

    const res = await api.getTrend({
      batch_id: batchId.value,
      keywords: topKeywords,
      time_dim: 'month'
    })
    trendData.value = res.data
  } catch (error) {
    console.error(error)
  }
}

const fetchCategoryData = async () => {
  if (!batchId.value) return

  try {
    const categories = ['开发', '运维', '测试', '产品', '数据']

    for (const category of categories) {
      const res = await api.getKeywords({
        batch_id: batchId.value,
        job_category: category,
        top_n: 10
      })
      categoryData.value[category] = res.keywords
    }
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
  await fetchKeywords()
  await fetchTrendData()
  await fetchCategoryData()
})
</script>

<style scoped>
.charts-view {
  max-width: 1400px;
  margin: 0 auto;
}

.chart-card {
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
</style>
