<template>
  <el-card class="card-view" shadow="always" :style="{ backgroundColor: randomColor(), color: config?.fontColor?.value }">
    <div style="display: flex; flex: 1; flex-wrap: wrap; justify-content: space-between; margin-top: 10px;" :style="{ color: config?.fontColor?.value }">
       <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
        <el-select v-model="selectedTimeRange" placeholder="选择时间范围">
          <el-option label="当天" value="today"></el-option>
          <el-option label="三天内" value="three_days"></el-option>
          <el-option label="一周内" value="one_week"></el-option>
          <el-option label="一月内" value="one_month"></el-option>
        </el-select>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
                  <h3>{{data && data.new_user ? data.new_user.today_new_users : 0 }}</h3>
            </div>
            <div class="enroll-text">今日注册用户</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
                <h3>{{ data && data.new_user ? data.new_user.three_days_new_users : 0 }}</h3>
            </div>
            <div class="enroll-text">三日注册用户</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{data && data.new_user? data.new_user.one_week_new_users :0 }}</h3>
            </div>
            <div class="enroll-text">一周内注册用户</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.new_user? data.new_user.one_month_new_users: 0 }}</h3>
            </div>
            <div class="enroll-text">一月内注册用户</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.new_guest? data.new_guest.today_new_guests : 0 }}</h3>
            </div>
            <div class="enroll-text">当天游客数</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.new_guest? data.new_guest.three_days_new_guests : 0 }}</h3>
            </div>
            <div class="enroll-text">三天内游客数</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.new_guest ? data.new_guest.one_week_new_guests : 0 }}</h3>
            </div>
            <div class="enroll-text">一周内游客数</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.new_guest? data.new_guest.one_month_new_guests :0 }}</h3>
            </div>
            <div class="enroll-text">一月内游客数</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.converion_rate? data.conversion_rate.guest_conversion_percentage_today : 0 }}%</h3>
            </div>
            <div class="enroll-text">当天游客转化率</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.conversion_rate? data.conversion_rate.guest_conversion_percentage_three_days : 0 }}%</h3>
            </div>
            <div class="enroll-text">三日内游客转化率</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{ data && data.conversion_rate? data.conversion_rate.guest_conversion_percentage_one_week : 0 }}%</h3>
            </div>
            <div class="enroll-text">一周内游客转化率</div>
          </div>
        </el-col>
      </div>
      <div style="flex: 1; min-width: 180px; max-width: 180px; height: 80px; display: flex;">
        <el-col :span="4" class="lightgreen-box">
          <div class="underline">
            <i class="el-icon-user"></i>
          </div>
        </el-col>
        <el-col :span="20" class="orange-box">
          <div class="enroll-time">
            <div class="enroll-number">
              <h3>{{data && data.conversion_rate? data.conversion_rate.guest_conversion_percentage_one_month:0 }}%</h3>
            </div>
            <div class="enroll-text">一月内游客转化率</div>
          </div>
        </el-col>
      </div>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 5,
  title: '用户新增统计',
  name: 'usersActive',
  icon: 'el-icon-user-solid',
  description: '用户新增以及活跃统计数据',
  height: 18,
  width: 20,
  isResizable: true,
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
  data () {
    return {
      data: {},
      selectedTimeRange: '',
      originalData: {}
    }
  },
  mounted () {
    this.initGet()
  },
  methods: {
    initGet () {
      request({
        url: '/api/system/dashboard/'
      }).then((res) => {
        this.data = res.data
      })
    },
    // 生成一个随机整数
    randomColor () {
      const color = [
        '#fffff'
      ]
      const ran = Math.floor(Math.random() * 4)
      return color[ran]
    }
  }
}
</script>

<style scoped lang="scss">
.card-view {
  // border-radius: 10px;
  color: $color-primary;
}
.enroll-number{
  color: $color-primary;
}
h3 {
  margin: 0;
}
.lightgreen-box {
  border-bottom: 2px solid;
  height: 60px;
  margin-bottom: 10px;
}

.underline i {
  font-size: 30px;
}

.orange-box {
  height: 60px;
  color: black;
  border-bottom: 2px solid rgb(242, 242, 242);
}

.enroll-time {
  margin-left: 10px;
}

.enroll-text {
  color: rgb(138, 138, 138);
}

.el-card {
  height: 100%;
}
</style>
