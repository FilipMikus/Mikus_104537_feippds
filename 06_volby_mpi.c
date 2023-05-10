#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <string.h>

#define MAX_LINE_LENGTH 80
#define DUMP_FACTOR 0.85

void print_ranks(double* ranks,  int vertices_count) {
    for (int i = 0; i < vertices_count; i++) {
        printf("Profile [%d] pagerank: %lf\n", i + 1, ranks[i]);
    }
}

int write_ranks_to_file(char *file_path, double* ranks,  int vertices_count, double running_time) {
    FILE *file = fopen(file_path, "w");
    if (!file) {
        perror(file_path);
        return EXIT_FAILURE;
    }
    for (int i = 0; i < vertices_count; i++) {
        fprintf(file, "Profile [%d] pagerank: %lf\n", i + 1, ranks[i]);
    }
    fprintf(file, "\n\nRuntime = %f\n", running_time);
    if (fclose(file)){
        perror(file_path);
        return EXIT_FAILURE;
    }
    return 0;
}

int **malloc_graph_matrix(int vertices_count) {
    int **graph_matrix = (int **) malloc(vertices_count * sizeof(int *));
    int i, j;
    for (i = 0; i < vertices_count; i++)
        graph_matrix[i] = (int *) malloc(vertices_count * sizeof(int));
    for (i = 0; i < vertices_count; i++)
        for (j = 0; j < vertices_count; j++)
            graph_matrix[i][j] = 0;
    return graph_matrix;
}

void free_graph_matrix(int **graph_matrix, int vertices_count) {
    for (int i = 0; i < vertices_count; i++)
        free(graph_matrix[i]);
    free(graph_matrix);
}

int get_vertices_count_from_file(char *file_path) {
    FILE *file = fopen(file_path, "r");
    if (!file) {
        perror(file_path);
        return EXIT_FAILURE;
    }
    char line[MAX_LINE_LENGTH], *ptr;
    int vertices_count;
    fgets(line, MAX_LINE_LENGTH, file);
    ptr = strtok(line, ":");
    ptr = strtok(NULL, ":");
    vertices_count = atoi(ptr);
    if (fclose(file)){
        perror(file_path);
        return EXIT_FAILURE;
    }
    return vertices_count;
}

int **get_graph_matrix_from_file(char *file_path, int vertices_count) {
    FILE *file = fopen(file_path, "r");
    if (!file) {
        perror(file_path);
        return NULL;
    }
    char line[MAX_LINE_LENGTH];
    int **graph_matrix = malloc_graph_matrix(vertices_count);
    char *node_id;
    int source_node_id_index, destination_node_id_index;
    fgets(line, MAX_LINE_LENGTH, file);
    while (fgets(line, MAX_LINE_LENGTH, file)) {
        node_id = strtok(line, " ");
        source_node_id_index = atoi(node_id);
        node_id = strtok(NULL, " ");
        destination_node_id_index = atoi(node_id);
        if (source_node_id_index != destination_node_id_index) {
            graph_matrix[source_node_id_index][destination_node_id_index] = 1;
        }
    }
    if (fclose(file)){
        free_graph_matrix(graph_matrix, vertices_count);
        perror(file_path);
        return NULL;
    }
    return graph_matrix;
}

int *get_counts_send(int processes_count, int vertices_count) {
    int *sendcounts = (int *) malloc(processes_count * sizeof(int));
    int i;
    double average = ((double) vertices_count) / ((double) processes_count);
    double last = 0.0;
    for (i = 0; i < processes_count; i++) {
        sendcounts[i] = ((int) (last + average)) - ((int) last);
        last += average;
    }
    return sendcounts;
}

int *get_displacements(int processes_count, const int *counts_send) {
    int *displs = (int *) malloc(processes_count * sizeof(int));
    int i;
    int j = 0;
    for (i = 0; i < processes_count; i++) {
        displs[i] = j;
        j += counts_send[i];
    }
    return displs;
}

double *pagerank_parallel(int process_id, int processes_count, int **graph_matrix, int vertices_count, int iterations_count) {
    double *ranks = (double *) malloc(vertices_count * sizeof(double));
    int i, j, k, l;
    for (i = 0; i < vertices_count; i++) {
        ranks[i] = 1.0 / vertices_count;
    }

    int *partitions_counts = get_counts_send(processes_count, vertices_count);
    int *partitions_indexes = get_displacements(processes_count, partitions_counts);
    int partition_vertices_count = partitions_counts[process_id];
    int partition_vertex_index = partitions_indexes[process_id];
    double *partition_ranks = (double *) malloc(partition_vertices_count * sizeof(double));
    double *tmp_ranks = (double *) malloc(partition_vertices_count * sizeof(double));
    double tmp_out_links_count;

    for (k = 0; k < iterations_count; k++) {

        MPI_Scatterv(ranks, partitions_counts, partitions_indexes, MPI_DOUBLE,
                     partition_ranks, partition_vertices_count, MPI_DOUBLE,
                     0, MPI_COMM_WORLD);

        for (i = partition_vertex_index; i < partition_vertex_index + partition_vertices_count; i++) {
            tmp_ranks[i - partition_vertex_index] = 0.0;
            for (j = 0; j < vertices_count; j++) {
                if (graph_matrix[j][i] == 1) {
                    tmp_out_links_count = 0.0;
                    for (l = 0; l < vertices_count; l++) {
                        tmp_out_links_count += graph_matrix[j][l];
                    }
                    tmp_ranks[i - partition_vertex_index] += ranks[j] / tmp_out_links_count;
                }
            }
            partition_ranks[i - partition_vertex_index] =
                    (1.0 - DUMP_FACTOR) + DUMP_FACTOR * tmp_ranks[i - partition_vertex_index];
        }

        MPI_Allgatherv(partition_ranks, partition_vertices_count, MPI_DOUBLE,
                       ranks, partitions_counts, partitions_indexes, MPI_DOUBLE,
                       MPI_COMM_WORLD);
    }

    free(partitions_counts);
    free(partitions_indexes);
    free(partition_ranks);
    free(tmp_ranks);

    return ranks;
}

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int process_id, processes_count;
    MPI_Comm_rank(MPI_COMM_WORLD, &process_id);
    MPI_Comm_size(MPI_COMM_WORLD, &processes_count);
    int vertices_count = get_vertices_count_from_file("test.txt");
    int **graph_matrix = get_graph_matrix_from_file("test.txt", vertices_count);

    double start_time = MPI_Wtime();

    double *ranks = pagerank_parallel(process_id, processes_count, graph_matrix, vertices_count, 3);

    double end_time = MPI_Wtime();
    double running_time = end_time - start_time;

    MPI_Finalize();

    if (process_id == 0) {
        print_ranks(ranks, vertices_count);
    }
    if (process_id == 0) {
        printf("\n\nRuntime = %f\n", running_time);
    }
    if (process_id == 0) {
        write_ranks_to_file("test_pagerank_output.txt", ranks, vertices_count, running_time);
    }

    free_graph_matrix(graph_matrix, vertices_count);
    free(ranks);

    return 0;
}