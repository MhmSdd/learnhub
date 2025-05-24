// ----------------------
// Theme Switcher
// ----------------------
document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;

    const icon = themeToggle.querySelector('i');
    const currentTheme = getCookie('theme') || 'light';
    setTheme(currentTheme);

    themeToggle.addEventListener('click', function () {
        const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        setCookie('theme', newTheme, 365);
    });

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (theme === 'dark') {
            icon.className = 'bi bi-sun-fill';
            themeToggle.childNodes[1].textContent = ' Light Mode';
        } else {
            icon.className = 'bi bi-moon-fill';
            themeToggle.childNodes[1].textContent = ' Dark Mode';
        }
    }

    // ----------------------
    // Load & Enroll in Courses
    // ----------------------
    if (typeof $ === 'undefined') {
        console.error("jQuery غير محمّل. تأكد من تحميله قبل script.js.");
        return;
    }

    const courseTable = $('#courses-table-body');
    const noCoursesMessage = $('#no-courses-message');

    if (courseTable.length > 0) {
        $.ajax({
            url: "/api/courses",
            method: "GET",
            xhrFields: { withCredentials: true },
            success: function (data) {
                if (!data.courses || data.courses.length === 0) {
                    noCoursesMessage.show();
                    return;
                }

                noCoursesMessage.hide();
                courseTable.empty();

                data.courses.forEach(course => {
                    courseTable.append(`
                        <tr data-course-id="${course.id}">
                            <td>${course.title}</td>
                            <td>${course.description}</td>
                            <td>
                                <button class="btn btn-primary enroll-btn" data-id="${course.id}">
                                    ${translations.enroll || 'Enroll'}
                                </button>
                                <button class="btn btn-danger unenroll-btn" data-id="${course.id}" style="display: none;">
                                    ${translations.unenroll || 'Unenroll'}
                                </button>
                            </td>
                        </tr>
                    `);
                });

                courseTable.on('click', '.enroll-btn', function() {
                    const button = $(this);
                    const courseId = button.data("id");
                    button.prop("disabled", true);

                    $.ajax({
                        url: "/ajax/enroll",
                        method: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({ course_id: courseId }),
                        xhrFields: { withCredentials: true },
                        success: function(response) {
                            alert(response.message);
                            button.hide();
                            button.siblings('.unenroll-btn').show();
                        },
                        error: function(xhr) {
                            alert(xhr.responseJSON?.message || (translations.errorEnroll || 'Error enrolling in course'));
                            button.prop("disabled", false);
                        }
                    });
                });

                courseTable.on('click', '.unenroll-btn', function() {
                    const button = $(this);
                    const courseId = button.data("id");
                    button.prop("disabled", true);

                    if (confirm(translations.confirmUnenroll || 'Are you sure you want to unenroll?')) {
                        $.ajax({
                            url: "/ajax/unenroll",
                            method: "POST",
                            contentType: "application/json",
                            data: JSON.stringify({ course_id: courseId }),
                            xhrFields: { withCredentials: true },
                            success: function(response) {
                                alert(response.message);
                                button.closest('tr').remove();
                            },
                            error: function(xhr) {
                                alert(xhr.responseJSON?.message || (translations.errorUnenroll || 'Error unenrolling from course'));
                                button.prop("disabled", false);
                            }
                        });
                    } else {
                        button.prop("disabled", false);
                    }
                });
            },
            error: function(xhr) {
                const errorMessage = xhr.status === 401 
                    ? (translations.loginRequired || 'You must be logged in to view courses.') 
                    : (translations.errorLoading || 'Error loading courses.');
                alert(errorMessage);
                if (xhr.status === 401) {
                    window.location.href = "/login";
                }
            }
        });
    }

    // ----------------------
    // Unenroll from Dashboard
    // ----------------------
    const enrolledCoursesList = $('#enrolled-courses');
    if (enrolledCoursesList.length > 0) {
        enrolledCoursesList.on('click', '.unenroll-btn', function() {
            const button = $(this);
            const courseId = button.data("id");
            button.prop("disabled", true);

            if (confirm(translations.confirmUnenroll || 'Are you sure you want to unenroll?')) {
                $.ajax({
                    url: "/ajax/unenroll",
                    method: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({ course_id: courseId }),
                    xhrFields: { withCredentials: true },
                    success: function(response) {
                        alert(response.message);
                        button.closest('li').remove();
                    },
                    error: function(xhr) {
                        alert(xhr.responseJSON?.message || (translations.errorUnenroll || 'Error unenrolling from course'));
                        button.prop("disabled", false);
                    }
                });
            } else {
                button.prop("disabled", false);
            }
        });
    }

    // ----------------------
    // Cookies
    // ----------------------
    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
    }

    function getCookie(name) {
        const cookies = decodeURIComponent(document.cookie).split(';');
        for (let cookie of cookies) {
            while (cookie.charAt(0) === ' ') cookie = cookie.substring(1);
            if (cookie.indexOf(name + '=') === 0) {
                return cookie.substring(name.length + 1);
            }
        }
        return "";
    }
});