document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

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

    function setEventListeners() {
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
                    console.log('Search request succeeded');
                    return response.text();
                }
                throw new Error('Network response was not ok.');
            }).then(html => {
                console.log('Search response received');
                document.body.innerHTML = html;
                setEventListeners();  // 이벤트 리스너를 다시 설정
                console.log('Tables limited');
                
                
                // 100개 출력
                $('#table-container table tbody tr').slice(0,100).show()
                $('#paper-table-container table tbody tr').slice(0,100).show()
            }).catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        };

        const plotButton = document.getElementById('plot-button');
        if (plotButton) {
            console.log('Plot button found');
            plotButton.addEventListener('click', function() {
                console.log('Plot button clicked');
                window.open('/plot', '_blank', 'width=1600,height=1600');
            });
        } else {
            console.log('Plot button not found');
        }

        // h1 클릭 시 검색 창 초기화
        const resetButton = document.getElementById('reset-button');
        if (resetButton) {
            resetButton.addEventListener('click', function() {
                // 체크박스 상태 초기화
                document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                    checkbox.checked = false;
                    const image = document.getElementById(`${checkbox.id}-image`);
                    if (image) {
                        image.classList.remove('checked');
                    }
                });

                // 검색 입력 필드 초기화 (만약 검색 필드가 있다면)
                const searchFields = document.querySelectorAll('input[type="text"]');
                searchFields.forEach(field => {
                    field.value = '';
                });

                console.log('Search and checkboxes reset');
            });
        } else {
            console.log('Reset button not found');
        }
    }

    setEventListeners();
});
