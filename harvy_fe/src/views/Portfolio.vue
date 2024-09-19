<template>
    <div class="portfolio-board">
        <div class="category-tabs">
            <button
                v-for="category in categories"
                :key="category"
                @click="selectedCategory = category"
                :class="{ active: selectedCategory === category }"
            >
                {{ category }}
            </button>
        </div>

        <div class="board-grid">
            <div v-for="board in paginatedBoards" :key="board.id" class="board-card" @click="openModal(board)">
                <div class="card-header">
                    <span class="category-tag">{{ board.pf_type }}</span>
                    <span class="options-menu" v-if="isAdmin" @click.stop>
                        <button @click="editBoard(board)">수정</button>
                        <button @click="deleteBoard(board.id)">삭제</button>
                    </span>
                </div>
                <h3 class="board-title">{{ board.board_title }}</h3>
                <p class="board-semidesc">{{ board.board_semidesc }}</p>
                <p class="board-date">{{ board.project_period }}</p>
            </div>
        </div>

        <!-- Pagination 추가 -->
        <div class="pagination">
            <button @click="goToFirstPage" :disabled="currentPage === 1" class="pagination-btn">&laquo;</button>
            <button @click="prevPage" :disabled="currentPage === 1" class="pagination-btn">&lt;</button>
            <button v-if="displayedPageNumbers[0] > 1" @click="goToPage(1)" class="pagination-btn">1</button>
            <span v-if="displayedPageNumbers[0] > 2">...</span>
            <button
                v-for="pageNumber in displayedPageNumbers"
                :key="pageNumber"
                @click="goToPage(pageNumber)"
                :class="['pagination-btn', { active: currentPage === pageNumber }]"
            >
                {{ pageNumber }}
            </button>
            <span v-if="displayedPageNumbers[displayedPageNumbers.length - 1] < totalPages - 1">...</span>
            <button
                v-if="displayedPageNumbers[displayedPageNumbers.length - 1] < totalPages"
                @click="goToPage(totalPages)"
                class="pagination-btn"
            >
                {{ totalPages }}
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-btn">&gt;</button>
            <button @click="goToLastPage" :disabled="currentPage === totalPages" class="pagination-btn">&raquo;</button>
        </div>

        <!-- Modal -->
        <div v-if="selectedBoard" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h2 class="modal-title">{{ selectedBoard.board_title }}</h2>
                <div class="project-meta">
                    <span class="project-type">{{ getProjectTypeLabel(selectedBoard.pf_type) }}</span>
                    <span class="project-period">{{ selectedBoard.project_period }}</span>
                </div>
                <div class="project-section">
                    <h3>프로젝트 소개</h3>
                    <ul v-html="formattedInfo"></ul>
                </div>
                <div class="project-section">
                    <h3>역할</h3>
                    <p>{{ selectedBoard.desc_role }}</p>
                </div>
                <div class="project-section">
                    <h3>주요 작업 내역</h3>
                    <ul v-html="formattedTasks"></ul>
                </div>
                <div class="project-section">
                    <h3>결과</h3>
                    <ul v-html="formattedResults"></ul>
                </div>
                <a
                    v-if="selectedBoard.pf_link"
                    :href="selectedBoard.pf_link"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="project-link"
                    >프로젝트 링크</a
                >
            </div>
        </div>

        <!-- 관리자용 추가 버튼 -->
        <button v-if="isAdmin" @click="showAddForm = true" class="add-button">새 포트폴리오 추가</button>

        <!-- 추가/수정 폼 모달 -->
        <div v-if="showAddForm" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeAddForm">&times;</span>
                <h2>{{ editingBoard ? '포트폴리오 수정' : '새 포트폴리오 추가' }}</h2>
                <form @submit.prevent="submitForm">
                    <input v-model="formData.board_title" placeholder="프로젝트 제목" required />
                    <textarea v-model="formData.board_semidesc" placeholder="프로젝트 간단 설명" required></textarea>
                    <textarea v-model="formData.desc_role" placeholder="역할"></textarea>
                    <textarea v-model="formData.desc_info" placeholder="프로젝트 소개"></textarea>
                    <textarea v-model="formData.desc_tasks" placeholder="주요 작업 내역"></textarea>
                    <textarea v-model="formData.desc_results" placeholder="결과"></textarea>
                    <input v-model="formData.pf_link" placeholder="프로젝트 링크" type="url" />
                    <input type="date" v-model="formData.pf_start_date" required />
                    <input type="date" v-model="formData.pf_end_date" />
                    <input type="number" v-model.number="formData.order_num" placeholder="표시 순서" />
                    <select v-model="formData.pf_type">
                        <option v-for="type in portfolioTypes" :key="type.value" :value="type.value">
                            {{ type.label }}
                        </option>
                    </select>
                    <button type="submit">{{ editingBoard ? '수정' : '추가' }}</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/services/api';

export default {
    name: 'PortfolioBoard',
    data() {
        return {
            categories: ['전체', 'AI', '기획', '웹 개발'],
            portfolioTypes: [
                { value: 'AI', label: 'AI' },
                { value: 'Planning', label: '기획' },
                { value: 'WEB_DEV', label: '웹 개발' },
            ],
            selectedCategory: '전체',
            boards: [],
            selectedBoard: null,
            isAdmin: false,
            showAddForm: false,
            formData: {
                board_title: '',
                board_semidesc: '',
                desc_role: '',
                desc_info: '',
                desc_tasks: '',
                desc_results: '',
                pf_link: '',
                pf_start_date: '',
                pf_end_date: '',
                order_num: null,
                pf_type: 'AI',
            },
            editingBoard: null,
            currentPage: 1,
            itemsPerPage: 6,
        };
    },
    computed: {
        filteredBoards() {
            let boards;
            if (this.selectedCategory === '전체') {
                boards = this.boards;
            } else {
                const categoryMap = {
                    AI: 'AI',
                    기획: 'Planning',
                    '웹 개발': 'WEB_DEV',
                };
                boards = this.boards.filter((board) => board.pf_type === categoryMap[this.selectedCategory]);
            }

            // order_num을 기준으로 정렬
            return boards.sort((a, b) => {
                // order_num이 없는 경우 가장 뒤로 보내기
                if (a.order_num === null) return 1;
                if (b.order_num === null) return -1;
                return b.order_num - a.order_num;
            });
        },
        formattedInfo() {
            return this.formatList(this.selectedBoard.desc_info);
        },
        formattedTasks() {
            return this.formatList(this.selectedBoard.desc_tasks);
        },
        formattedResults() {
            return this.formatList(this.selectedBoard.desc_results);
        },
        paginatedBoards() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredBoards.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.filteredBoards.length / this.itemsPerPage);
        },
        displayedPageNumbers() {
            const range = 2; // 현재 페이지 양쪽에 표시할 페이지 수
            let start = Math.max(1, this.currentPage - range);
            let end = Math.min(this.totalPages, this.currentPage + range);

            if (start > 1) {
                if (start > 2) {
                    start++; // 1 ... 표시를 위한 공간
                }
            }
            if (end < this.totalPages) {
                if (end < this.totalPages - 1) {
                    end--; // ... lastPage 표시를 위한 공간
                }
            }

            let pages = [];
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        },
        totalItems() {
            return this.filteredBoards.length;
        },
    },
    methods: {
        async fetchBoards() {
            try {
                const response = await api.get('portfolios/');
                if (response.data && Array.isArray(response.data)) {
                    this.boards = response.data;
                } else {
                    console.error('Unexpected data format:', response.data);
                }
            } catch (error) {
                console.error('Error fetching portfolio boards:', error);
            }
        },
        async checkAdminStatus() {
            try {
                this.isAdmin = await api.checkAdmin();
                console.log('Is admin:', this.isAdmin);
            } catch (error) {
                console.error('Admin check failed:', error);
                this.isAdmin = false;
            }
        },
        formatDate(dateString) {
            return dateString ? new Date(dateString).toLocaleDateString('ko-KR') : '';
        },
        openModal(board) {
            this.selectedBoard = board;
        },
        closeModal() {
            this.selectedBoard = null;
        },
        closeAddForm() {
            this.showAddForm = false;
            this.editingBoard = null;
            this.resetForm();
        },
        resetForm() {
            this.formData = {
                board_title: '',
                board_semidesc: '',
                desc_role: '',
                desc_info: '',
                desc_tasks: '',
                desc_results: '',
                pf_link: '',
                pf_start_date: '',
                pf_end_date: '',
                order_num: null,
                pf_type: this.portfolioTypes[0].value,
            };
        },
        getProjectTypeLabel(type) {
            const typeMap = {
                AI: 'AI',
                Planning: '기획',
                WEB_DEV: '웹 개발',
            };
            return typeMap[type] || type;
        },
        async submitForm() {
            try {
                const formData = { ...this.formData };
                for (let key in formData) {
                    if (formData[key] === '') {
                        if (key === 'pf_end_date') {
                            delete formData[key]; // pf_end_date가 비어있으면 필드 자체를 제거
                        } else {
                            formData[key] = null;
                        }
                    }
                }
                if (formData.pf_end_date) {
                    formData.pf_end_date = new Date(formData.pf_end_date).toISOString().split('T')[0];
                }
                if (formData.pf_start_date) {
                    formData.pf_start_date = new Date(formData.pf_start_date).toISOString().split('T')[0];
                }
                console.log('Submitting form data:', formData); // 디버깅용
                let response;
                if (this.editingBoard) {
                    response = await api.put(`portfolios/${this.editingBoard.id}/`, formData);
                } else {
                    response = await api.post('portfolios/', formData);
                }
                console.log('Server response:', response.data); // 디버깅용
                await this.fetchBoards();
                this.closeAddForm();
                alert(this.editingBoard ? '포트폴리오가 수정되었습니다.' : '새 포트폴리오가 추가되었습니다.');
            } catch (error) {
                console.error('Form submission error:', error);
                if (error.response) {
                    console.error('Error data:', error.response.data);
                    console.error('Error status:', error.response.status);
                    let errorMessage = '알 수 없는 오류가 발생했습니다.';
                    if (error.response.data.pf_end_date) {
                        errorMessage = `종료일 오류: ${error.response.data.pf_end_date[0]}`;
                    }
                    alert(`오류 발생: ${errorMessage}`);
                } else {
                    alert('서버와의 통신 중 오류가 발생했습니다.');
                }
            }
        },
        editBoard(board) {
            this.editingBoard = board;
            this.formData = { ...board };
            this.showAddForm = true;
        },
        async deleteBoard(boardId) {
            if (confirm('정말로 이 포트폴리오를 삭제하시겠습니까?')) {
                try {
                    await api.delete(`portfolios/${boardId}/`);
                    await this.fetchBoards();
                } catch (error) {
                    console.error('Delete error:', error);
                }
            }
        },
        // 결과나 작업 내역이 한 줄로 나오는 것 방지
        formatList(text) {
            if (!text) return '';
            return text
                .split('-')
                .filter((item) => item.trim())
                .map((item) => `<li>${item.trim()}</li>`)
                .join('');
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        goToPage(page) {
            this.currentPage = page;
        },
        goToFirstPage() {
            this.currentPage = 1;
        },
        goToLastPage() {
            this.currentPage = this.totalPages;
        },
    },
    // 보고 있는 화면을 초기화
    watch: {
        selectedCategory() {
            this.currentPage = 1;
        },
    },
    mounted() {
        this.fetchBoards();
        this.checkAdminStatus();
    },
};
</script>

<!-- v-html 디렉티브 스타일이 적용되지 않는 문제로 따로 설정 -->
<style>
.project-section ul {
    list-style-type: disc;
    padding-left: 20px;
}

.project-section li {
    margin-bottom: 10px;
    line-height: 1; /* 행 간격 크게 증가 */
}
</style>

<style scoped>
.portfolio-board {
    max-width: 1200px;
    margin: 50px auto 0;
    padding: 20px;
    font-family: 'NanumSquare', sans-serif !important;
}

.category-tabs {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
    background-color: #f7f7f7;
    border-radius: 20px;
    padding: 5px;
}

.category-tabs button {
    font-size: 15px;
    background: none;
    border: none;
    padding: 10px 20px;
    margin: 0 5px;
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.category-tabs button.active {
    background-color: #3498db;
    color: #f2f2f2;
    /* font-weight: bold; */
    font-size: 15px;
}

.board-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.board-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.board-card:hover {
    transform: translateY(-5px);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
}

.category-tag {
    background-color: #f2f2f2;
    padding: 3px 8px;
    border-radius: 10px;
    font-size: 0.8em;
}

.options-menu {
    font-weight: bold;
    color: #888;
}

.board-title {
    padding: 0 15px;
    margin: 10px 0;
    font-size: 1.2em;
}

.board-semidesc {
    padding: 0 15px;
    margin-bottom: 10px;
    font-size: 0.9em;
    color: #666;
}

.board-date {
    padding: 0 15px;
    font-size: 0.8em;
    color: #888;
}

.modal {
    position: fixed;
    z-index: 1200;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-content {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 15px;
    width: 90%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal-title {
    font-size: 24px;
    color: #333;
    margin-bottom: 15px;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.add-button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

form {
    display: flex;
    flex-direction: column;
}

form input,
form textarea,
form select {
    margin-bottom: 10px;
    padding: 5px;
}

form button {
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    cursor: pointer;
}

.project-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    font-size: 14px;
}

.project-type,
.project-period {
    background-color: #f0f0f0;
    padding: 5px 10px;
    border-radius: 15px;
    color: #555;
}

.project-section {
    margin-bottom: 25px;
}

.project-section ul {
    list-style-type: disc;
    padding-left: 20px;
}

.project-section h3 {
    font-size: 18px;
    color: #3498db;
    margin-bottom: 10px;
    border-left: 3px solid #3498db;
    padding-left: 10px;
}

.project-section p,
.project-section div {
    line-height: 1.6;
    color: #444;
}

.project-link {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.project-link:hover {
    background-color: #2980b9;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
    transition: color 0.3s ease;
}

.close:hover {
    color: #333;
}

/* 스크롤바 스타일링 */
.modal-content::-webkit-scrollbar {
    width: 8px;
}

.modal-content::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.modal-content::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
    background: #555;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    font-family: 'Arial', sans-serif;
}

.pagination-btn {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #dddddd;
    width: 32px;
    height: 32px;
    margin: 0 2px;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

.pagination-btn:hover {
    background-color: #f0f0f0;
}

.pagination-btn.active {
    background-color: #007bff;
    color: white;
    border-color: #007bff;
}

.pagination-btn:disabled {
    color: #cccccc;
    cursor: not-allowed;
}

@media (max-width: 768px) {
    .board-grid {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
}

@media (max-width: 480px) {
    .board-grid {
        grid-template-columns: 1fr;
    }
}
</style>
