<template>
  <div class="report-view">
    <el-card shadow="never" class="matrix-card">
      <template #header>
        <div class="card-header">
          <div class="card-header-left">
            <el-icon :size="18" color="var(--primary)"><Grid /></el-icon>
            <span>岗位技能矩阵分析</span>
          </div>
        </div>
      </template>

      <el-table
        :data="matrixData"
        border
        stripe
        v-loading="loading"
        style="width: 100%"
        size="small"
      >
        <el-table-column
          v-for="col in columns"
          :key="col"
          :prop="col"
          :label="col"
          :min-width="col === '岗位类别' ? 120 : 90"
        >
          <template #default="{ row }">
            <el-tag v-if="col !== '岗位类别' && row[col] > 0" size="small" type="primary" effect="plain">
              {{ row[col] }}
            </el-tag>
            <span v-else-if="col === '岗位类别'" class="category-cell">{{ row[col] }}</span>
            <span v-else class="empty-cell">-</span>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!matrixData.length && !loading" description="暂无矩阵数据，请先进行关键词分析" :image-size="80" />
    </el-card>

    <el-card shadow="never" class="heatmap-card">
      <template #header>
        <div class="card-header">
          <div class="card-header-left">
            <el-icon :size="18" color="var(--primary)"><DataAnalysis /></el-icon>
            <span>技能分布可视化</span>
          </div>
        </div>
      </template>

      <div ref="heatmapRef" class="heatmap-container"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Grid, DataAnalysis } from '@element-plus/icons-vue'
import { api } from '@/api/index'
import * as echarts from 'echarts'

const batchId = ref(localStorage.getItem('batchId') || '')
const loading = ref(false)
const columns = ref([])
const matrixData = ref([])
const heatmapRef = ref(null)
let heatmapChart = null

const fetchMatrixTable = async () => {
  if (!batchId.value) return

  loading.value = true
  try {
    const res = await api.getMatrixTable({
      batch_id: batchId.value,
      top_n: 10
    })
    columns.value = res.columns
    matrixData.value = res.data
  } catch (error) {
    ElMessage.error('获取矩阵数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchMatrixData = async () => {
  if (!batchId.value) return

  try {
    const res = await api.getMatrix({
      batch_id: batchId.value,
      top_n: 10
    })

    renderHeatmap(res.matrix)
  } catch (error) {
    console.error(error)
  }
}

const renderHeatmap = (data) => {
  if (!heatmapRef.value || !data.length) return

  heatmapChart = echarts.init(heatmapRef.value)

  const jobs = [...new Set(data.map(d => d.job))]
  const skills = [...new Set(data.map(d => d.skill))]

  const heatmapData = []
  data.forEach(d => {
    const jobIndex = jobs.indexOf(d.job)
    const skillIndex = skills.indexOf(d.skill)
    heatmapData.push([skillIndex, jobIndex, d.count])
  })

  const option = {
    title: {
      text: '岗位-技能热力图',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      position: 'top',
      formatter: (params) => {
        return `${skills[params.value[0]]} - ${jobs[params.value[1]]}: ${params.value[2]}`
      }
    },
    grid: {
      left: '15%',
      right: '10%',
      bottom: '15%',
      top: 60
    },
    xAxis: {
      type: 'category',
      data: skills,
      splitArea: { show: true },
      axisLabel: { rotate: 45 }
    },
    yAxis: {
      type: 'category',
      data: jobs,
      splitArea: { show: true }
    },
    visualMap: {
      min: 0,
      max: Math.max(...data.map(d => d.count)),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 10,
      inRange: {
        color: ['#f0f9ff', '#0066cc', '#003366']
      }
    },
    series: [{
      name: '技能频次',
      type: 'heatmap',
      data: heatmapData,
      label: {
        show: true
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }

  heatmapChart.setOption(option)
}

onMounted(() => {
  fetchMatrixTable()
  fetchMatrixData()

  window.addEventListener('resize', () => {
    heatmapChart?.resize()
  })
})
</script>

<style scoped>
.report-view {
  max-width: 1400px;
  margin: 0 auto;
}

.matrix-card,
.heatmap-card {
  border-radius: var(--radius-lg);
  border: none;
}

.heatmap-card {
  margin-top: 20px;
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

.heatmap-container {
  width: 100%;
  height: 500px;
}

.category-cell {
  font-weight: 500;
  color: var(--text-primary);
}

.empty-cell {
  color: var(--text-light);
  font-size: 12px;
}
</style>
