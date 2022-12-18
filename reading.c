#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Driver Code
int main()
{
	// Substitute the full file path
	// for the string file_path
	FILE* fp = fopen("../Files/stock.csv", "r");

	if (!fp)
		printf("Can't open file\n");

	else {
		char buffer[1000];

		int row = 0;
		int column = 0;

		while (fgets(buffer,
					1024, fp)) {
			column = 1;
			row++;

			// To avoid printing of column
			// names in file can be changed
			// according to need
			if (row == 1)
				continue;

			// Splitting the data
			char* value = strtok(buffer, ", ");

			while (value) {
				// Column 1
				if (column == 0) {
					printf("Cash initial:");
				}

				// Column 2
				if (column == 1) {
					printf("\tFruit :");
				}

				// Column 3
				if (column == 2) {
					printf("\tPrice:");
				}
                // Column 4
				if (column == 3) {
					printf("\tQuantity :");
				}

				printf("%s", value);
				value = strtok(NULL, ", ");
				column++;
			}

			printf("\n");
		}

		// Close the file
		fclose(fp);
	}
	return 0;
}
