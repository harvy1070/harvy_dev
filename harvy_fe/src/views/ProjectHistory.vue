<template>
    <div class="project-history">
        <h2>참여한 프로젝트 소개</h2>
        <div v-if="loading">로딩 중...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else class="timeline">
            <div v-for="item in timeline" :key="item.id" class="timeline-item">
                <div class="timeline-date">
                    <span class="date-circle"></span>
                    {{ formatDate(item.date) }}
                </div>
                <div class="timeline-content">
                    <h3>{{ item.title }}</h3>
                    <div class="timeline-company-role-order" v-if="item.company || item.role || item.order_company">
                        {{ item.company }}{{ item.company && item.role ? ' (' + item.role + ')' : item.role }}
                        {{ (item.company || item.role) && item.order_company ? ' / ' : '' }}
                        {{ item.order_company }}
                    </div>
                    <p>{{ item.description }}</p>
                    <div class="timeline-type">{{ item.type }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/services/api';

export default {
    name: 'ProjectHistory',
    data() {
        return {
            timeline: [],
            loading: true,
            error: null,
        };
    },
    mounted() {
        this.fetchTimeline();
    },
    methods: {
        async fetchTimeline() {
            try {
                const response = await api.get('timeline/');
                this.timeline = response.data;
                this.loading = false;
            } catch (error) {
                this.error = '타임라인 데이터를 불러오는 데 실패했습니다.';
                this.loading = false;
                console.error('Error fetching timeline:', error);
            }
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'long' };
            return new Date(dateString).toLocaleDateString('ko-KR', options);
        },
    },
};
</script>

<style scoped>
.project-history {
    margin-top: 50px !important;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    /* align-items: center; */
}

.timeline {
    position: relative;
    padding: 20px 0;
}

.timeline::before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    left: 20px;
    width: 2px;
    background: #3498db;
}

.timeline-item {
    position: relative;
    margin-bottom: 30px;
    padding-left: 50px;
}

.timeline-date {
    font-weight: bold;
    margin-bottom: 10px;
    color: #3498db;
    position: relative;
}

.date-circle {
    position: absolute;
    left: -40px;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    background-color: #3498db;
    border-radius: 50%;
    z-index: 1;
}

.timeline-content {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.timeline-content h3 {
    margin-top: 0;
    color: #2c3e50;
}

.timeline-type {
    margin-top: 10px;
    font-style: italic;
    color: #7f8c8d;
}

.timeline-company-role {
    font-weight: bold;
    color: #34495e;
    margin-bottom: 10px;
}

.timeline-company-role-order {
    font-weight: bold;
    color: #3d8eff;
    margin-bottom: 10px;
}

@media (max-width: 768px) {
    .timeline::before {
        left: 10px;
    }

    .timeline-item {
        padding-left: 30px;
    }

    .date-circle {
        left: -30px;
        width: 16px;
        height: 16px;
    }
}
</style>
