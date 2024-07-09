document.addEventListener('DOMContentLoaded', () => {
    // 초기화할 것이 있으면 여기에 추가
});

function search() {
    const keyword = document.getElementById('keyword').value.trim();
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const categories = Array.from(document.querySelectorAll('input[name="category"]:checked')).map(cb => cb.value);

    // 검색어 필수 입력 검사
    if (!keyword) {
        alert('검색어를 입력하세요.');
        return;
    }

    // fetch 요청 생성
    const url = `/search?keyword=${encodeURIComponent(keyword)}&start_date=${startDate}&end_date=${endDate}&categories=${categories.join(',')}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function displayResults(data) {
    const resultContainer = document.getElementById('search-results');
    resultContainer.innerHTML = '';

    if (data.length === 0) {
        resultContainer.innerHTML = '<p>검색 결과가 없습니다.</p>';
    } else {
        // 검색 결과 표 생성
        const table = document.createElement('table');
        table.classList.add('result-table');
        const header = table.createTHead();
        const headerRow = header.insertRow();
        headerRow.innerHTML = `
            <th>출원번호</th>
            <th>출원일자</th>
            <th>출원인</th>
            <th>특허명</th>
        `;

        const tbody = table.createTBody();
        data.forEach(item => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${item.ap_num}</td>
                <td>${item.application_date}</td>
                <td class="applicant-link" data-applicant="${item.applicant}">${item.applicant}</td>
                <td>${item.title}</td>
            `;
        });

        resultContainer.appendChild(table);

        // 출원인 정보 불러오기
        fetch(`/applicants?keyword=${encodeURIComponent(data[0].applicant)}`)
            .then(response => response.json())
            .then(applicants => {
                displayApplicants(applicants);
            })
            .catch(error => {
                console.error('Error fetching applicants:', error);
            });
    }
}

function displayApplicants(applicants) {
    const applicantContainer = document.getElementById('applicant-info');
    applicantContainer.innerHTML = '';

    const heading = document.createElement('h3');
    heading.textContent = '출원인 정보';
    applicantContainer.appendChild(heading);

    if (applicants.length === 0) {
        applicantContainer.innerHTML += '<p>출원인 정보가 없습니다.</p>';
    } else {
        // 출원인 별 출원 건수 계산
        const applicantCounts = {};
        applicants.forEach(applicant => {
            if (!applicantCounts[applicant.name]) {
                applicantCounts[applicant.name] = 0;
            }
            applicantCounts[applicant.name]++;
        });

        // 출원인 정보와 출원 건수 출력
        Object.keys(applicantCounts).forEach(applicantName => {
            const p = document.createElement('p');
            p.innerHTML = `
                <a href="https://www.wanted.co.kr/search?query=${encodeURIComponent(applicantName)}&tab=overview" target="_blank">${applicantName}</a> (${applicantCounts[applicantName]} 건)
            `;
            applicantContainer.appendChild(p);
        });
    }
}


// 출원인 클릭 시 Wanted 링크로 이동
document.addEventListener('click', event => {
    const applicantLink = event.target.closest('.applicant-link');
    if (applicantLink) {
        const applicantName = applicantLink.dataset.applicant;
        const url = `https://www.wanted.co.kr/search?query=${encodeURIComponent(applicantName)}&tab=overview`;
        window.open(url, '_blank');
    }
});
