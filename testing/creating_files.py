def generate_big_file(filename='big_test_file.txt', size_mb=50):
    line = "This is a test line for file sharing application testing.\n"
    lines_needed = (size_mb * 1024 * 1024) // len(line)

    with open(filename, 'w') as f:
        for _ in range(lines_needed):
            f.write(line)

    print(f"Generated {filename} with ~{size_mb} MB")

if __name__ == "__main__":
    generate_big_file()
