<template>
    <div class="qna">
        <h1 class="h1">PM Chatbot이란? (개발중입니다)</h1>
        <h2 class="h2">
            Portfolio Matching Chatbot으로 사용자가 챗봇과의 상호작용을 통해<br />
            사용자가 원하는 포트폴리오를 추천받을 수 있도록 하는 시스템입니다.<br />
        </h2>
        <h3 class="h3">
            대화 기반 추천 <br />
            사용자는 간단한 대화를 통해 기술 스택, 프로젝트 유형 등 개인의 요구사항을 입력하고, <br />
            PM Chatbot은 이를 분석하여 가장 적합한 포트폴리오를 찾아드립니다. <br /><br />
            AI 기술 활용 <br />
            PM Chatbot은 자연어 처리(NLP)와 머신러닝 기술을 기반으로 사용자의 입력을 이해하고, <br />
            맞춤형 포트폴리오를 실시간으로 추천합니다. <br /><br />
            효율적 탐색 <br />
            복잡한 검색 과정을 거치지 않고, 챗봇과의 대화를 통해 쉽고 빠르게 원하는 결과를 얻을 수 있습니다.
        </h3>
    </div>
</template>

<script>
export default {
    name: 'QnAPage',
};
</script>

<style scoped>
.qna {
    margin-top: 150px;
    margin-left: 200px;
}
.h1 {
    color: #346aff;
}
.h2 {
    color: #313131;
}
.h3 {
    color: #747474;
}
</style>
