<template>
  <el-card
    class="card-view"
    :style="{ backgroundColor: randomColor() }"
    shadow="always"
  >
    <div class="card-header">
      <div class="card-content-label">数据库统计</div>
      <el-button
        class="real-time"
        type="primary"
        size="small"
        @click="switchDatabase"
      >
        <i class="el-icon-arrow-down"></i> 切换
      </el-button>
    </div>
    <div class="card-content">
      <div v-if="activeDatabase" class="database-info">
        <div class="database-name">{{ activeDatabase.name }}</div>
        <div class="info-item">
          <div class="info-label" style="display: inline;">数量：</div>
          <div class="info-value" style="display: inline;">{{ activeDatabase.count }}</div>
          <br>
          <div class="info-label" style="display: inline;">占用空间：</div>
          <div class="info-value" style="display: inline;">{{ activeDatabase.space }}</div>
        </div>
      </div>
    </div>

  </el-card>

</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 4,
  title: '数据库统计',
  name: 'databaseTotal',
  icon: 'el-icon-coin',
  description: '数据库统计',
  height: 14,
  width: 16,
  isResizable: true,
  data() {
    return {
      databases: [
        {
          name: 'chatai_admin',
          count: 0,
          space: ''
        },
        {
          name: 'chatai',
          count: 0,
          space: ''
        }
      ],
      activeDatabaseIndex: 0
    }
  },
  computed: {
    activeDatabase() {
      return this.databases[this.activeDatabaseIndex]
    }
  },
  config: {
    color: {
      label: '背景颜色',
      type: 'color',
      value: '',
      placeholder: '颜色为空则随机变换颜色'
    },
    fontColor: {
      label: '字体颜色',
      type: 'color',
      value: '',
      placeholder: '请选择字体颜色'
    }
  },
  props: {
    config: {
      type: Object,
      required: false
    }
  },
  methods: {
    switchDatabase() {
      this.activeDatabaseIndex = (this.activeDatabaseIndex + 1) % this.databases.length
      this.fetchDatabaseStats(this.activeDatabase.name)
    },
    fetchDatabaseStats(database) {
      // Make the API request to fetch the database statistics for the given database
      request({
        url: '/api/system/database_total/'
      }).then((res) => {
        const { databases } = res.data;
        if (databases && Array.isArray(databases)) {
          this.databases = databases;
          const databaseStats = databases.find(db => db.name === database);
          if (databaseStats) {
            this.activeDatabase.count = databaseStats.count;
            this.activeDatabase.space = databaseStats.space;
          }
        }
      })
    },
    randomColor() {
      if (this.config?.color?.value) {
        return this.config.color.value
      }
      return this.$util.randomColor()
    }
  },
  mounted() {
    this.fetchDatabaseStats(this.activeDatabase.name)
  }
}
</script>

<style scoped lang="scss">
.card-view {
  //border-radius: 10px;
  color: $color-primary;

  .card-content {
    .card-content-label {
      font-size: 0.8em;
    }

    .card-content-value {
      margin-top: 5px;
      font-size: 1.5em;
      //font-weight: bold;
    }
  }

  .attachment-value {
    margin-top: 5px;
    font-size: 1.5em;
    font-weight: bold;
  }

  .el-icon-document-copy {
    font-size: 12px;
  }

  .el-icon-s-flag {
    font-size: 12px;
  }
}

.real-time {
  background: rgb(53, 59, 86);
  color: #ffffff;
  font-size: 14px;
  font-style: normal;
  padding: 0 7px 0 7px;
  border-radius: 4px;
  position: absolute;
  right: 20px;
  top: 20px;
}

.el-card {
  height: 100%;
}

.absolute-right {
  position: absolute;
  right: 30px;
}

.absolute-left {
  position: absolute;
}
</style>
