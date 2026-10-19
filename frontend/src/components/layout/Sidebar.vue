<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <span class="sidebar-title">导航菜单</span>
    </div>
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      router
      :unique-opened="true"
    >
      <el-menu-item index="/data">
        <el-icon><Document /></el-icon>
        <span>数据管理</span>
      </el-menu-item>
      <el-menu-item index="/analysis">
        <el-icon><TrendCharts /></el-icon>
        <span>技能分析</span>
      </el-menu-item>
      <el-menu-item index="/charts">
        <el-icon><PieChart /></el-icon>
        <span>图表展示</span>
      </el-menu-item>
      <el-menu-item index="/report">
        <el-icon><DocumentCopy /></el-icon>
        <span>分析报告</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Document, TrendCharts, PieChart, DocumentCopy } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar {
  width: 220px;
  background: var(--bg-sidebar);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 20px 20px 12px;
}

.sidebar-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(255, 255, 255, 0.4);
}

.sidebar-menu {
  border: none;
  background: transparent;
  flex: 1;
}

.sidebar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.65);
  margin: 2px 8px;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.sidebar-menu .el-menu-item:hover {
  background: var(--bg-sidebar-hover);
  color: rgba(255, 255, 255, 0.9);
}

.sidebar-menu .el-menu-item.is-active {
  background: var(--primary);
  color: #fff;
  font-weight: 500;
}

.sidebar-menu .el-menu-item .el-icon {
  color: inherit;
}
</style>
