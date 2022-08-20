import os
dir_name = "frames3"

done = False
i = 0
new_file_name = "frames"
with open(f"{new_file_name}.txt", "w") as new_file:

    while not done:
        file_name = f"frame{i}"
        file_path = f"{dir_name}/{file_name}.txt"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                new_file.write(file.readline())
                new_file.write("\n")
            print("working on file", i)
            i += 1
            file.close()

        else:
            done = True
            print("done!")
            new_file.close()

