// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    function limitTableRows() {
        const table = document.querySelector('#table-container table');
        if (!table) return;

        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            if (index >= 10) {
                row.style.display = 'none';
            }
        });

        const container = document.querySelector('#table-container');
        container.addEventListener('scroll', () => {
            if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
                rows.forEach((row, index) => {
                    if (index >= 10 && row.style.display === 'none') {
                        row.style.display = '';
                    }
                });
            }
        });
    }

    function limitPaperTableRows() {
        const table = document.querySelector('#paper-table-container table');
        if (!table) return;

        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            if (index >= 10) {
                row.style.display = 'none';
            }
        });

        const container = document.querySelector('#paper-table-container');
        container.addEventListener('scroll', () => {
            if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
                rows.forEach((row, index) => {
                    if (index >= 10 && row.style.display === 'none') {
                        row.style.display = '';
                    }
                });
            }
        });
    }

    function resetForm() {
        // 모든 필터 초기화
        document.getElementById("filter_type").value = "patent";
        document.getElementById("search_keyword").value = "";
        document.getElementById("start_date").value = "2013-01-01";
        document.getElementById("end_date").value = new Date().toISOString().split('T')[0]; // 오늘 날짜로 설정

        // 모든 체크박스 초기화
        const checkboxes = document.querySelectorAll("input[type='checkbox']");
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

        // 이미지 클릭 토글 초기화
        const icons = document.querySelectorAll('.category-icon');
        icons.forEach(icon => {
            icon.classList.remove('checked');
        });

        // 검색 결과 지우기
        const tableContainer = document.getElementById("table-container");
        if (tableContainer) {
            tableContainer.innerHTML = "";
        }

        const paperTableContainer = document.getElementById("paper-table-container");
        if (paperTableContainer) {
            paperTableContainer.innerHTML = "";
        }

        // 출원인 정보 초기화
        const topTablesContainer = document.querySelector(".top-tables");
        if (topTablesContainer) {
            topTablesContainer.innerHTML = "";
        }
    }

    limitTableRows();
    limitPaperTableRows();

    document.getElementById('search-form').onsubmit = function(event) {
        event.preventDefault();
        var form = event.target;

        fetch(form.action, {
            method: form.method,
            body: new FormData(form),
        }).then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok.');
        }).then(html => {
            document.body.innerHTML = html;
            limitTableRows();
            limitPaperTableRows();
            window.open('/plot', '_blank', 'width=800,height=600');

            // 재설정 이벤트 리스너 추가
            document.getElementById("homeButton").addEventListener("click", resetForm);
        }).catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    };

    const homeButton = document.getElementById("homeButton");
    homeButton.addEventListener("click", resetForm);


});
