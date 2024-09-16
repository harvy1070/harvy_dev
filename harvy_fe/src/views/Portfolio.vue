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
            <div v-for="board in filteredBoards" :key="board.id" class="board-card" @click="openModal(board)">
                <div class="card-header">
                    <span class="category-tag">{{ board.category }}</span>
                    <span class="options-menu" v-if="isAdmin" @click.stop>
                        <button @click="editBoard(board)">수정</button>
                        <button @click="deleteBoard(board.id)">삭제</button>
                    </span>
                </div>
                <h3 class="board-title">{{ board.board_title }}</h3>
                <p class="board-semidesc">{{ board.board_semidesc }}</p>
                <p class="board-date">{{ formatDate(board.pf_date) }}</p>
            </div>
        </div>

        <!-- Modal -->
        <div v-if="selectedBoard" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h2>{{ selectedBoard.board_title }}</h2>
                <p>{{ selectedBoard.board_semidesc }}</p>
                <div v-html="selectedBoard.board_desc"></div>
                <p>프로젝트 일자: {{ formatDate(selectedBoard.pf_date) }}</p>
                <a :href="selectedBoard.pf_link" target="_blank" rel="noopener noreferrer">프로젝트 링크</a>
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
                    <input v-model="formData.board_title" placeholder="제목" required />
                    <textarea v-model="formData.board_semidesc" placeholder="간단 설명" required></textarea>
                    <textarea v-model="formData.board_desc" placeholder="상세 설명"></textarea>
                    <input v-model="formData.pf_link" placeholder="프로젝트 링크" />
                    <input type="date" v-model="formData.pf_date" required />
                    <input type="number" v-model.number="formData.order_num" placeholder="표시 순서" />
                    <select v-model="formData.category">
                        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
                    </select>
                    <button type="submit">{{ editingBoard ? '수정' : '추가' }}</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'PortfolioBoard',
    data() {
        return {
            categories: ['전체', '기획', 'AI', '웹 개발'],
            selectedCategory: '전체',
            boards: [],
            selectedBoard: null,
            isAdmin: false,
            showAddForm: false,
            formData: {
                board_title: '',
                board_semidesc: '',
                board_desc: '',
                pf_link: '',
                pf_date: '',
                order_num: null,
                category: '기획',
            },
            editingBoard: null,
        };
    },
    computed: {
        filteredBoards() {
            if (this.selectedCategory === '전체') {
                return this.boards;
            }
            return this.boards.filter((board) => board.category === this.selectedCategory);
        },
    },
    methods: {
        async fetchBoards() {
            try {
                const response = await axios.get('/api/portfolioboard/');
                this.boards = response.data;
            } catch (error) {
                console.error('Error fetching portfolio boards:', error);
            }
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString('ko-KR');
        },
        openModal(board) {
            this.selectedBoard = board;
        },
        closeModal() {
            this.selectedBoard = null;
        },
        async checkAdminStatus() {
            try {
                const response = await axios.get('/api/check-admin/');
                this.isAdmin = response.data.isAdmin;
            } catch (error) {
                console.error('Admin check failed:', error);
            }
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
                board_desc: '',
                pf_link: '',
                pf_date: '',
                order_num: null,
                category: '기획',
            };
        },
        async submitForm() {
            try {
                if (this.editingBoard) {
                    await axios.put(`/api/portfolioboard/${this.editingBoard.id}/`, this.formData);
                } else {
                    await axios.post('/api/portfolioboard/', this.formData);
                }
                this.fetchBoards();
                this.closeAddForm();
            } catch (error) {
                console.error('Form submission error:', error);
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
                    await axios.delete(`/api/portfolioboard/${boardId}/`);
                    this.fetchBoards();
                } catch (error) {
                    console.error('Delete error:', error);
                }
            }
        },
    },
    mounted() {
        this.fetchBoards();
        this.checkAdminStatus();
    },
};
</script>

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
    z-index: 1;
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
    background-color: #fefefe;
    padding: 20px;
    border-radius: 12px;
    width: 80%;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
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
