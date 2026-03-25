 const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebarClose = document.getElementById('sidebarClose');
        const overlay = document.getElementById('overlay');
        
        function openSidebar() {
            sidebar.classList.add('open');
            overlay.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
        
        function closeSidebar() {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
        
        sidebarToggle.addEventListener('click', openSidebar);
        sidebarClose.addEventListener('click', closeSidebar);
        overlay.addEventListener('click', closeSidebar);
        
        // Close sidebar when clicking on a link (for mobile)
        document.querySelectorAll('.sidebar .nav-link').forEach(link => {
            link.addEventListener('click', closeSidebar);
        });
        
        // Sale banner click event
        document.getElementById('saleBanner').addEventListener('click', function() {
            alert('Redirecting to the $1 Sale page!');
            // In a real implementation, you would redirect to the sale page
            // window.location.href = '/sale';
        });
        
        // Category click events
        document.querySelectorAll('.category-card').forEach(card => {
            card.addEventListener('click', function(e) {
                e.preventDefault();
                const category = this.getAttribute('data-category');
                alert(`Redirecting to ${category.toUpperCase()} category page!`);
                // In a real implementation, you would redirect to the category page
                // window.location.href = `/category/${category}/`;
            });
        });
        
        // Scroll down animation
        document.querySelector('.scroll-down').addEventListener('click', function() {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        });
        
        // Add animation to category cards on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        // Observe category cards
        document.querySelectorAll('.category-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s, transform 0.5s';
            observer.observe(card);
        });
