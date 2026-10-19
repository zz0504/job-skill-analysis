<template>
  <div ref="chartRef" :style="{ width: width, height: height }"></div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  },
  title: {
    type: String,
    default: '技能趋势变化'
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '400px'
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance || !Object.keys(props.data).length) return
  
  const keywords = Object.keys(props.data)
  const timePeriods = new Set()
  
  keywords.forEach(keyword => {
    Object.keys(props.data[keyword]).forEach(period => {
      timePeriods.add(period)
    })
  })
  
  const sortedPeriods = Array.from(timePeriods).sort()
  
  const series = keywords.map(keyword => {
    const data = sortedPeriods.map(period => {
      return props.data[keyword][period] || 0
    })
    
    return {
      name: keyword,
      type: 'line',
      smooth: true,
      data: data
    }
  })
  
  const option = {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: keywords,
      top: 30
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: 80,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: sortedPeriods
    },
    yAxis: {
      type: 'value',
      name: '出现次数'
    },
    series: series
  }
  
  chartInstance.setOption(option)
}

watch(() => props.data, () => {
  updateChart()
}, { deep: true })

onMounted(() => {
  initChart()
  
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>
