import os


def generate_html(base_dir):
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Slokas Recitations by Jagadguru Shri Kripalu Maharaj</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; background: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #4B0082; }
            .category { margin-bottom: 20px; }
            .category h2 {
                cursor: pointer;
                background-color: #f0f0f0;
                color: #404040;
                padding: 10px;
                border-radius: 5px;
                margin: 0;
                font-size: 1.2em;
                display: flex;
                align-items: center;
                justify-content: flex-start;
            }
            .category h2::before {
                content: '▶'; /* Dropdown arrow */
                margin-right: 10px;
                font-size: 1.2em;
                transition: transform 0.3s;
            }
            .category.open h2::before {
                content: '▼'; /* Down arrow icon when expanded */
                transform: rotate(90deg);
            }
            .files {
                display: none;
                margin-left: 20px;
                padding: 10px;
                border-left: 2px solid #007bff;
            }
            .files.show {
                display: block;
            }
            .files div { margin-bottom: 10px; }
            audio { width: 100%; margin-bottom: 10px; }
            .file-item { display: flex; align-items: center; gap: 2px; }
            .file-item a {
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
                white-space: nowrap; /* Prevent wrapping */
                overflow: auto-x; /* Hide excess content */
                text-overflow: ellipsis; /* Add ellipsis */
                width: calc(40% - 50px); /* Adjust width as needed */
            }
            .file-item a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Slokas Recitations by Kripalu Maharaj</h1>
    '''

    # Generate HTML for directory and files
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in sorted(dirs) if d not in ('.git', '.', '.idea')]

        if not files:
            continue

        category = os.path.relpath(root, base_dir)
        html_content += f'<div class="category">\n'
        html_content += f'    <h2>{category}</h2>\n'
        html_content += f'    <div id="{category.replace(os.sep, "_")}" class="files">\n'
        for file in sorted(files):
            if file.endswith('.mp3'):
                file_path = os.path.join(category, file)
                html_content += f'        <div class="file-item">\n'
                html_content += f'            <a href="{file_path}" target="_blank">{file}</a>\n'
                html_content += f'            <audio controls preload="none">\n'
                html_content += f'                <source src="{file_path}" type="audio/mpeg">\n'
                html_content += f'                Your browser does not support the audio element.\n'
                html_content += f'            </audio>\n'
                html_content += f'        </div>\n'
        html_content += '    </div>\n'
        html_content += '</div>\n'

    html_content += '''
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const categories = document.querySelectorAll('.category h2');
            categories.forEach(header => {
                header.addEventListener('click', function() {
                    const filesDiv = this.nextElementSibling;
                    filesDiv.classList.toggle('show');
                    this.parentElement.classList.toggle('open');
                });
            });

            // Lazy loading
            const files = document.querySelectorAll('.files');
            const observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const audioElements = entry.target.querySelectorAll('audio');
                        audioElements.forEach(audio => {
                            if (audio.preload !== 'auto') {
                                audio.preload = 'auto';
                            }
                        });
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '100px'
            });

            files.forEach(fileContainer => {
                observer.observe(fileContainer);
            });
        });
    </script>
    </body>
    </html>
    '''

    with open('index.html', 'w') as file:
        file.write(html_content)


if __name__ == "__main__":
    generate_html('.')
