from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from forum.models import Category, Thread, Post
from django.utils import timezone
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with test data for the forum'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create test users
        self.stdout.write('Creating users...')
        users = []
        user_data = [
            {'email': 'alice@example.com', 'username': 'alice', 'bio': 'Tech enthusiast and developer'},
            {'email': 'bob@example.com', 'username': 'bob', 'bio': 'Love discussing new technologies'},
            {'email': 'charlie@example.com', 'username': 'charlie', 'bio': 'Forum moderator'},
            {'email': 'diana@example.com', 'username': 'diana', 'bio': 'Coffee lover and coder'},
            {'email': 'eve@example.com', 'username': 'eve', 'bio': 'Open source contributor'},
            {'email': 'frank@example.com', 'username': 'frank', 'bio': 'DevOps engineer'},
            {'email': 'grace@example.com', 'username': 'grace', 'bio': 'UI/UX designer'},
            {'email': 'henry@example.com', 'username': 'henry', 'bio': 'Data scientist'},
        ]
        
        for data in user_data:
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'bio': data['bio']
                }
            )
            if created:
                # nosemgrep: python.django.security.audit.unvalidated-password.unvalidated-password
                # Test data with intentionally simple password for development/seeding
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  Created user: {user.username}')
            users.append(user)
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {
                'name': 'General Discussion',
                'slug': 'general',
                'description': 'General topics and casual conversations',
                'icon': '💬',
                'order': 1
            },
            {
                'name': 'Tech Talk',
                'slug': 'tech',
                'description': 'Discuss programming, software, and technology',
                'icon': '💻',
                'order': 2
            },
            {
                'name': 'Web Development',
                'slug': 'webdev',
                'description': 'Frontend, backend, and full-stack development',
                'icon': '🌐',
                'order': 3
            },
            {
                'name': 'Mobile Development',
                'slug': 'mobile',
                'description': 'iOS, Android, and cross-platform development',
                'icon': '📱',
                'order': 4
            },
            {
                'name': 'Off-Topic',
                'slug': 'offtopic',
                'description': 'Everything else that doesn\'t fit other categories',
                'icon': '🎲',
                'order': 5
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'  Created category: {category.name}')
            categories.append(category)
        
        # Create threads
        self.stdout.write('Creating threads...')
        threads_data = [
            {
                'title': 'Welcome to the forum!',
                'content': 'Welcome everyone! This is a place for discussing various topics. Feel free to introduce yourself and start conversations.',
                'category': categories[0],
                'is_pinned': True
            },
            {
                'title': 'What are you working on this week?',
                'content': 'Share what projects or tasks you\'re focusing on this week. Let\'s motivate each other!',
                'category': categories[0]
            },
            {
                'title': 'Best Python web framework in 2024?',
                'content': 'I\'m starting a new project and trying to decide between Django, Flask, and FastAPI. What are your experiences with these frameworks?',
                'category': categories[1]
            },
            {
                'title': 'Docker vs Kubernetes - When to use what?',
                'content': 'Can someone explain the differences and when you should use Docker alone vs when you need Kubernetes?',
                'category': categories[1]
            },
            {
                'title': 'React 18 - What\'s new?',
                'content': 'Just upgraded to React 18. The concurrent rendering features are interesting. Anyone else tried the new hooks?',
                'category': categories[2]
            },
            {
                'title': 'Tailwind CSS vs traditional CSS',
                'content': 'I\'ve been using traditional CSS for years. Is Tailwind CSS worth learning? What are the pros and cons?',
                'category': categories[2]
            },
            {
                'title': 'Building REST APIs with Django REST Framework',
                'content': 'Share your tips and tricks for building efficient REST APIs with DRF. What are your favorite packages?',
                'category': categories[2]
            },
            {
                'title': 'Flutter vs React Native in 2024',
                'content': 'Planning to start mobile development. Which framework would you recommend for a web developer?',
                'category': categories[3]
            },
            {
                'title': 'iOS SwiftUI tutorial recommendations',
                'content': 'Looking for good SwiftUI tutorials for beginners. Any recommendations?',
                'category': categories[3]
            },
            {
                'title': 'Best code editor setup',
                'content': 'Share your editor setup, plugins, themes, and configurations!',
                'category': categories[1]
            },
            {
                'title': 'Remote work tips and tricks',
                'content': 'How do you stay productive while working from home? Share your best practices!',
                'category': categories[4]
            },
            {
                'title': 'Coffee or tea while coding?',
                'content': 'What\'s your preferred beverage while coding? ☕🍵',
                'category': categories[4]
            },
            {
                'title': 'Weekend project showcase',
                'content': 'Built something cool over the weekend? Share it here!',
                'category': categories[0]
            },
            {
                'title': 'Learning resources for beginners',
                'content': 'Curating a list of great resources for people just starting their coding journey. Please contribute!',
                'category': categories[1]
            },
            {
                'title': 'GraphQL vs REST - The eternal debate',
                'content': 'Let\'s discuss when to use GraphQL vs REST APIs. What are your experiences?',
                'category': categories[2]
            },
        ]
        
        threads = []
        for thread_data in threads_data:
            thread, created = Thread.objects.get_or_create(
                title=thread_data['title'],
                defaults={
                    **thread_data,
                    'author': random.choice(users)
                }
            )
            if created:
                self.stdout.write(f'  Created thread: {thread.title}')
            threads.append(thread)
        
        # Create posts (replies)
        self.stdout.write('Creating posts...')
        posts_data = [
            'Great point! I totally agree with this perspective.',
            'Thanks for sharing! This is really helpful.',
            'I have a different opinion on this. Here\'s why...',
            'Can you elaborate more on this?',
            'This is exactly what I was looking for!',
            'Has anyone else experienced this?',
            'I found a solution that worked for me...',
            'Interesting approach! Never thought of it that way.',
            'Here\'s a link to more information about this topic.',
            'This reminds me of a similar discussion we had...',
            'I\'ve been using this in production for months now.',
            'One thing to keep in mind is...',
            'Great tutorial! Helped me a lot.',
            'I think there might be a better way to do this.',
            'Anyone know if this works with the latest version?',
            'Just wanted to add my two cents here...',
            'This solved my problem, thank you!',
            'Could you provide more examples?',
            'I\'m having a similar issue. Did you find a solution?',
            'Bookmarking this for later reference!',
            'This is a game changer for me!',
            'I would approach this differently...',
            'Great discussion everyone!',
            'Let me know if you need any help with this.',
            'I wrote a blog post about this topic.',
            'This is still relevant in 2024!',
            'Anyone tried this with TypeScript?',
            'The documentation mentions this as well.',
            'I ran into the same problem last week.',
            'Here\'s an alternative solution...',
            'Make sure to check the official docs.',
            'This works perfectly, tested it myself!',
            'One caveat to watch out for...',
            'I would be careful with this approach.',
            'Brilliant explanation! Very clear.',
            'This is on my learning list now.',
            'Thanks for starting this discussion!',
            'I\'ll have to try this out.',
            'My team has been using this successfully.',
            'Great resource, adding to my bookmarks!',
            'This is the future of web development!',
            'I prefer the old way but this is interesting.',
            'Can confirm this works great.',
            'This tutorial is outdated now.',
            'Updated version available here...',
            'Performance might be an issue with large datasets.',
            'Security implications should be considered.',
            'This is best practice these days.',
            'Anyone know of alternatives?',
            'I built something similar last month.',
        ]
        
        post_count = 0
        for thread in threads:
            # Create 2-5 random posts per thread
            num_posts = random.randint(2, 5)
            for i in range(num_posts):
                post, created = Post.objects.get_or_create(
                    thread=thread,
                    author=random.choice(users),
                    content=random.choice(posts_data),
                    defaults={
                        'created_at': timezone.now() - timezone.timedelta(
                            days=random.randint(0, 30),
                            hours=random.randint(0, 23)
                        )
                    }
                )
                if created:
                    post_count += 1
        
        self.stdout.write(f'  Created {post_count} posts')
        
        # Update thread view counts randomly
        self.stdout.write('Updating thread statistics...')
        for thread in threads:
            thread.views_count = random.randint(10, 500)
            thread.save()
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(f'Created:')
        self.stdout.write(f'  - {len(users)} users')
        self.stdout.write(f'  - {len(categories)} categories')
        self.stdout.write(f'  - {len(threads)} threads')
        self.stdout.write(f'  - {post_count} posts')
        self.stdout.write('')
        self.stdout.write('Test user credentials (all passwords: password123):')
        for user in users[:5]:
            self.stdout.write(f'  - Email: {user.email} / Username: {user.username}')
