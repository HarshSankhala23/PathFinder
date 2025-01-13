# PathFinder
PathFinder is a modern, fast, and visually appealing directory and file fuzzing tool designed for penetration testers and bug bounty hunters. With real-time results, a beautiful progress bar, and multi-threaded execution, PathFinder makes it easy to discover hidden paths and files on a web server.


![image](https://github.com/user-attachments/assets/43499ae7-4555-4a05-90ff-4cc6ed8a1596)


### 🔥 Features
	
- Multi-threaded Speed: Blazing-fast fuzzing with configurable thread support.
- Real-Time Results: Instant display of discovered paths with HTTP status codes.
- Modern UI: Sleek and colorful progress bar with percentage completion and elapsed time.
- Customizable: Set thread count, request timeouts, and use any wordlist.
- Error Handling: Resilient to network issues, ensuring smooth execution.
- Lightweight: Minimal dependencies for quick setup and use



#### Install Dependencies
```
pip3 install -r requirements.txt
```

#### Usage
```
git clone https://github.com/yourusername/pathfinder.git
cd pathfinder

python3 pathfinder.py https://example.com -w /path/to/wordlist.txt -t 20 --timeout 3
```
