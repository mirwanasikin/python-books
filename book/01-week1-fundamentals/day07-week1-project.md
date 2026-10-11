# Day 07 — Week 1 Project

Keywords: All from Week 1 (`None, True, False, and, or, not, is, in, if, elif, else, match, case, for, while, break, continue, pass, import, as, def, return, lambda, yield, global, nonlocal, try, except, finally, raise, assert, with, from, del`)

## Project: system_report.py

Build a script that collects system information and generates a formatted report using only concepts learned in Week 1.

### Starter Code
```python
#!/usr/bin/env python3
"""
System Report Generator
Collects OS information and generates a formatted report
"""

def get_os_info():
    """Get basic OS information"""
    import os
    import platform
    
    info = {}
    info['system'] = platform.system()
    info['release'] = platform.release()
    info['version'] = platform.version()
    info['machine'] = platform.machine()
    info['processor'] = platform.processor()
    
    return info

def get_memory_info():
    """Get memory information with psutil fallback"""
    try:
        import psutil
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used,
            'free': mem.free
        }
    except ImportError:
        # Fallback if psutil not available
        return {'error': 'psutil not installed'}

def get_disk_info(path='/'):
    """Get disk information with psutil fallback"""
    try:
        import psutil
        disk = psutil.disk_usage(path)
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': (disk.used / disk.total) * 100
        }
    except ImportError:
        # Fallback if psutil not available
        return {'error': 'psutil not installed'}

def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def main():
    """Main function to generate system report"""
    print("=" * 50)
    print("SYSTEM REPORT")
    print("=" * 50)
    
    # Get OS info
    os_info = get_os_info()
    print(f"System: {os_info['system']} {os_info['release']}")
    print(f"Version: {os_info['version']}")
    print(f"Machine: {os_info['machine']}")
    print(f"Processor: {os_info['processor']}")
    print()
    
    # Get memory info
    mem_info = get_memory_info()
    if 'error' not in mem_info:
        print("MEMORY INFORMATION")
        print("-" * 30)
        print(f"Total: {format_bytes(mem_info['total'])}")
        print(f"Available: {format_bytes(mem_info['available'])}")
        print(f"Used: {format_bytes(mem_info['used'])}")
        print(f"Free: {format_bytes(mem_info['free'])}")
        print(f"Usage: {mem_info['percent']:.1f}%")
    else:
        print("MEMORY INFORMATION")
        print("-" * 30)
        print(mem_info['error'])
    print()
    
    # Get disk info
    disk_info = get_disk_info('/')
    if 'error' not in disk_info:
        print("DISK INFORMATION")
        print("-" * 30)
        print(f"Total: {format_bytes(disk_info['total'])}")
        print(f"Used: {format_bytes(disk_info['used'])}")
        print(f"Free: {format_bytes(disk_info['free'])}")
        print(f"Usage: {disk_info['percent']:.1f}%")
    else:
        print("DISK INFORMATION")
        print("-" * 30)
        print(disk_info['error'])

if __name__ == "__main__":
    main()
```

### Tasks
1. **Read + type every example** in the starter code above
2. **Implement the functions** using only Week 1 concepts (no advanced features)
3. **Test the script** on your Linux system
4. **Add error handling** for cases where commands fail
5. **Format output** clearly and consistently

### Success Criteria
- Script runs without errors on Linux
- Displays OS information correctly
- Shows memory information (either via psutil or graceful fallback)
- Shows disk information (either via psutil or graceful fallback)
- Uses only concepts from Week 1 days
- Output is clearly formatted and readable

### DevOps Context
This script represents a common DevOps task: gathering system information for monitoring, debugging, or inventory purposes. In production environments, such reports might be:
- Generated regularly via cron jobs
- Sent to monitoring systems
- Used for capacity planning
- Attached to support tickets for troubleshooting

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day07 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day07 -v` — see `tests/day07/test_day07.py`
