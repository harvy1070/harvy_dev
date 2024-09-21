<template>
    <div class="project-history">
        <h2 class="section-title"><i class="fas fa-project-diagram"></i> 참여 프로젝트</h2>
        <div v-if="loading" class="loading">로딩 중...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="timeline">
            <div v-for="item in timeline" :key="item.id" class="timeline-item">
                <div class="timeline-date">
                    <span class="date-circle"></span>
                    {{ formatDate(item.date) }}
                </div>
                <div class="timeline-content">
                    <h3 class="project-title">
                        {{ item.title }}
                        <span v-if="item.order_company" class="order-company">{{ item.order_company }}</span>
                    </h3>
                    <div class="company-role" v-if="item.company || item.role">
                        {{ item.company }}{{ item.company && item.role ? ' / ' + item.role : item.role }}
                    </div>
                    <p class="project-description">{{ item.description }}</p>
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

<style>
.project-history {
    font-family: 'NanumSquare', sans-serif !important;
}
</style>

<style scoped>
.project-history {
    max-width: 800px;
    margin: 50px auto 0;
    padding: 20px;
    font-family: 'Arial', sans-serif;
}

.section-title {
    font-size: 1.5rem;
    color: #3498db;
    margin-bottom: 30px;
    text-align: left;
    display: flex;
    align-items: center;
}

.section-title i {
    margin-right: 10px;
    color: #3498db;
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
    background: #e0e0e0;
}

.timeline-item {
    position: relative;
    margin-bottom: 40px;
    padding-left: 50px;
}

.timeline-date {
    font-weight: 600;
    margin-bottom: 10px;
    color: #3498db;
    position: relative;
}

.date-circle {
    position: absolute;
    left: -35px;
    top: 50%;
    transform: translateY(-50%);
    width: 12px;
    height: 12px;
    background-color: #3498db;
    border-radius: 50%;
    z-index: 1;
}

.timeline-content {
    background: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.timeline-content:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.project-title {
    margin-top: 0;
    color: #2c3e50;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.order-company {
    font-size: 0.8rem;
    color: #7f8c8d;
    font-weight: normal;
}

.company-role {
    font-weight: 600;
    color: #3498db;
    margin-bottom: 10px;
    font-size: 0.9rem;
}

.project-description {
    color: #34495e;
    line-height: 1.6;
    font-size: 0.95rem;
    margin-bottom: -10px;
}

.timeline-type {
    margin-top: 10px;
    /* font-style: italic; */
    color: #7f8c8d;
    font-size: 0.85rem;
}

@media (max-width: 768px) {
    .timeline::before {
        left: 10px;
    }

    .timeline-item {
        padding-left: 35px;
    }

    .date-circle {
        left: -25px;
    }
}

.loading,
.error {
    text-align: center;
    padding: 20px;
    font-size: 1.1rem;
    color: #7f8c8d;
}
</style>
