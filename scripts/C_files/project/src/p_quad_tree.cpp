/*----------------------------------------------------------------------------
 | Authors:
 |     - Weizhi Xu   (weizhix)  752454
 |     - Zijun Chen  (zijunc3)  813190
 -----------------------------------------------------------------------------*/
#include <algorithm>
#include "p_quad_tree.hpp"

#define TIMER
static const int TIMER_CNT = 5;
static const char* PHASE_STR[TIMER_CNT] = {"Load Balance", "Construct Tree", "Broadcast Tree", "Compute forces", "Send/Recv particles"};

void qt_p_sim(int n_particle, int n_steps, float dt, particle_t *ps, float grav, FILE *f_out, bool is_full_out) {
    int m_size, m_rank;
    MPI_Comm_size(MPI_COMM_WORLD, &m_size);
    MPI_Comm_rank(MPI_COMM_WORLD, &m_rank);

#ifdef TIMER
    float durations[TIMER_CNT] = {0.0f};
    uint64_t start;
#endif
    if (m_rank == ROOT_NODE) {
        printf("MPI_size: %d, OPENMP_threads: %d\n", m_size, omp_get_max_threads());
    }

    // the number of particles is small, switch to sequential
    // if (log2(n_particle) < m_size) {
    //     qt_sim(n_particle, n_steps, time_step, ps, grav, f_out, is_full_out);
    //     return ;
    // }

    const float boundary = qt_find_boundary(n_particle, ps);

    // init an array of integers representing the index of the particle in 'ps'
    // as the order in the original particle array needs to be preserved
    int *ps_idx = new int [n_particle];
    if (ps_idx == NULL) {
        fprintf(stderr, "Unable to allocate memory\n");
        exit(1);
    }

    for (int step = 0; step < n_steps; step++) {

        /* balance load using ORB */
#ifdef TIMER
        if (m_rank == ROOT_NODE) start = GetTimeStamp();
#endif
        int work_rank_assign = 0;

        int orb_lvl = (int)(ceil(log2(m_size)));
        // int orb_lvl = 2;
        // if (m_rank == ROOT_NODE) {
        //     printf("Using ORB level: %d\n", orb_lvl);
        // }

        // counter for how many particles within the boundary
        int p_cnt = 0;
        for (int i = 0; i < n_particle; i++) {
            if (!qt_is_out_of_boundary(&(ps[i]), boundary)) {
                // printf("%d: \t%f\t%f\n", p_cnt, ps[i].pos.x, ps[i].pos.y);
                ps_idx[p_cnt++] = i;
            }
        }

        // for (int i = 0; i < n_particle; i++) {
        //     printf("%d: %f\n", ps_idx[i], ps[ps_idx[i]].pos.x);
        // }

        qt_ORB_node_t *orb_root = qt_new_ORB_node(-boundary, boundary, boundary*2, boundary*2);
        orb_root->l = 0;
        orb_root->r = p_cnt-1;
        qt_ORB_with_level(orb_root, ps, ps_idx, 0, p_cnt-1, 0, orb_lvl, &work_rank_assign, m_size);

        qt_print_ORB_tree(orb_root, 0, ps, ps_idx);

#ifdef TIMER
        if (m_rank == ROOT_NODE) durations[0] += GetTimeSpentInSeconds(start);
#endif

        /* construct quad tree (BH) on each node */
#ifdef TIMER
        if (m_rank == ROOT_NODE) start = GetTimeStamp();
#endif
        qt_p_construct_BH(ps, ps_idx, orb_root, m_rank);
#ifdef TIMER
        if (m_rank == ROOT_NODE) durations[1] += GetTimeSpentInSeconds(start);
#endif

        /* send/recv tree */
#ifdef TIMER
        if (m_rank == ROOT_NODE) start = GetTimeStamp();
#endif
        qt_p_bcast(orb_root, m_rank);
#ifdef TIMER
        if (m_rank == ROOT_NODE) durations[2] += GetTimeSpentInSeconds(start);
#endif

        /* compute force */
#ifdef TIMER
        if (m_rank == ROOT_NODE) start = GetTimeStamp();
#endif
        qt_p_compute_force(orb_root, ps, ps_idx, dt, grav, m_rank);
#ifdef TIMER
        if (m_rank == ROOT_NODE) durations[3] += GetTimeSpentInSeconds(start);
#endif
        /* gather all particles to root for output */
#ifdef TIMER
        if (m_rank == ROOT_NODE) start = GetTimeStamp();
#endif
        qt_p_gather_particle(orb_root, ps, ps_idx, m_rank);
#ifdef TIMER
        if (m_rank == ROOT_NODE) durations[4] += GetTimeSpentInSeconds(start);
#endif

        if (m_rank == ROOT_NODE) {
            if (step == (n_steps - 1) || is_full_out) {
                output_particle_pos(n_particle, ps, f_out);
            }
        }
    }

#ifdef TIMER
    // output all durations in average
    if (m_rank == ROOT_NODE) {
        for (int i = 0; i < TIMER_CNT; i++) {
            printf("%s: %f sec\n", PHASE_STR[i], durations[i]/n_steps);
        }

    }
#endif
    
    delete [] ps_idx;
}

float get_v(particle_t p, bool is_horizon) {
    return is_horizon ? p.pos.y : p.pos.x;
}

void qt_ORB_with_level(qt_ORB_node_t *node, particle_t *ps, int *idx, int l, int r, int d, int lvl, int *w_r, int size) {
    // printf("lvl %d: %d, %d\n", d, l, r);

    if (d == lvl || r == l) {
        node->end_node = true;
        node->work_rank = ((*w_r)++ % size);
        return ;
    }

    int n = r-l+1;
    int k = ((n & 1) ? (n+1)/2 : n/2);

    bool is_horizon = d&1;

    float median = qt_quick_select(ps, idx+l, n, is_horizon, k);
    
    

    // for (int i = l; i <= l+k-1; i++) {
    //     auto v = get_v(ps[idx[i]], is_horizon);
    //     assert(v <= median);
    // }
    // assert( get_v(ps[idx[l+k]], is_horizon) == median );
    // for (int i = l+k+1; i <= r; i++) {
    //     auto v = get_v(ps[idx[i]], is_horizon);
    //     assert(v >= median);
    // } 

    // printf("is_horizon: %d ,median: %f\n", is_horizon, median);

    d++;

    qt_ORB_node_t *new_node;

    // TODO: openmp
    if (l <= l+k-1) {
        // divide the space horizontally, thus, the height, y_len shrinks
        if (is_horizon) {
            new_node = qt_new_ORB_node(node->min_pos.x, node->min_pos.y,
                                       node->len.x, (node->min_pos.y)-median);
        } else {
            new_node = qt_new_ORB_node(node->min_pos.x, node->min_pos.y,
                                       median-(node->min_pos.x), node->len.y);
        }
        new_node->l = l;
        new_node->r = l+k-1;
        node->left = new_node;
        qt_ORB_with_level(new_node, ps, idx, l, l+k-1, d, lvl, w_r, size);
        // {   
        //     for (int i = l; i <= l+k-1; ++i) {
        //         auto& pos = ps[idx[i]].pos;
        //         auto& node = *new_node;

        //         printf("pos.x = %f, pos.y = %f, node.x = %f, node.y = %f, node.len.x = %f, node.len.y = %f \n", 
        //                 pos.x, pos.y, node.min_pos.x, node.min_pos.y, node.len.x, node.len.y);
        //         if (pos.x < node.min_pos.x || pos.x >= node.min_pos.x + node.len.x) {
        //             assert(false);
        //         }
        //         if (pos.y > node.min_pos.y || pos.y <= node.min_pos.y - node.len.y) {
        //             assert(false);
        //         }
        //     }
        // }


    }
    if (l+k <= r) {
        if (is_horizon) {
            new_node = qt_new_ORB_node(node->min_pos.x, median,
                                       node->len.x, median - (node->min_pos.y - node->len.y));
        } else {
            new_node = qt_new_ORB_node(median, node->min_pos.y,
                                       (node->min_pos.x + node->len.x) - median, node->len.y);
        }
        new_node->l = l+k;
        new_node->r = r;
        node->right = new_node;
        qt_ORB_with_level(new_node, ps, idx, l+k, r, d, lvl, w_r, size);
        // {   
        //     for (int i = l+k; i <= r; ++i) {
        //         auto& pos = ps[idx[i]].pos;
        //         auto& node = *new_node;

        //         printf("pos.x = %f, pos.y = %f, node.x = %f, node.y = %f, node.len.x = %f, node.len.y = %f \n", 
        //                 pos.x, pos.y, node.min_pos.x, node.min_pos.y, node.len.x, node.len.y);
        //         if (pos.x < node.min_pos.x || pos.x >= node.min_pos.x + node.len.x) {
        //             assert(false);
        //         }
        //         if (pos.y > node.min_pos.y || pos.y <= node.min_pos.y - node.len.y) {
        //             assert(false);
        //         }
        //     }
        // }
    }
}

class QtComparator {
    public: 
        QtComparator(particle_t *ps, bool is_horizon) {
            this->ps = ps;
            this->is_horizon = is_horizon;
        }

        bool operator () (const int &lhs, const int &rhs) {
            if (is_horizon) {
                return get_value(lhs) > get_value(rhs);
            } else {
                return get_value(lhs) < get_value(rhs);
            }
        }

        float get_value(int idx) {
            auto& pos = ps[idx].pos;
            return is_horizon ? pos.y : pos.x;
        }

    private:
        particle_t *ps;
        bool is_horizon;
}; 



// This code block implements the QuickSelect algorithm to find the median particle according to its x/y coordinate.
float qt_quick_select(particle_t *ps, int *idx, int n, bool is_horizon, int k) {
    QtComparator qt_comp(ps, is_horizon);
    std::nth_element(&idx[0], &idx[0] + k - 1, &idx[0] + n, qt_comp);
    return qt_comp.get_value(idx[k-1]);
}

// float qt_quick_select(particle_t *ps, int *idx, int l, int r, size_t offset, int k) {
//     int i = l, j = r;
//     int pivot = l + ((r-l) >> 1);
//     float med = qt_ps_idx_to_xy(ps, idx[pivot], offset);

//     while (i < j) {
//         // printf("====================\n");
//         // for (int k = l; k <= r; k++) {
//         //     printf("%d: %f\n", idx[k], qt_ps_idx_to_xy(ps, idx[k], offset));
//         // }
//         // printf("pivot: %d, med: %f, [%d, %d]\n", pivot, med, i, j);
//         while ( i < j && qt_offset_gt(ps, idx, pivot, i, offset)) i++;
//         while ( i < j && !qt_offset_gt(ps, idx, pivot, j, offset)) j--;

//         if (i < j) std::swap(idx[i], idx[j]);
//         // pivot = i;
//         // med = qt_ps_idx_to_xy(ps, idx[pivot], offset);

//         // printf("pivot: %d, med: %f, [%d, %d]\n", pivot, med, i, j);
//         // for (int k = l; k <= r; k++) {
//         //     printf("%d: %f\n", idx[k], qt_ps_idx_to_xy(ps, idx[k], offset));
//         // }

//     }
//     // pivot = i;

//     // printf("i: %d, j: %d\n", i, j);
//     // printf("med: %f\n", qt_ps_idx_to_xy(ps, idx[pivot], offset));

//     if (i - l + 1 == k) {
//         // printf("return\n");
//         return qt_ps_idx_to_xy(ps, idx[i], offset);
//     } else if (i - l + 1 < k) {
//         // printf("right part\n");
//         return qt_quick_select(ps, idx, i+1, r, offset, k - (i-l+1));
//     } else {
//         // printf("left part\n");
//         return qt_quick_select(ps, idx, l, i-1, offset, k);
//     }
// }

inline float qt_ps_idx_to_xy(particle_t *ps, int i, size_t offset) {
    return *(float *)(((char *)&(ps[i].pos))+offset);
}

bool qt_offset_gt(particle_t *ps, int *idx, int l, int r, size_t offset) {
    if (qt_ps_idx_to_xy(ps, idx[l], offset) > qt_ps_idx_to_xy(ps, idx[r], offset))  {
        return true;
    } else {
        return false;
    }
}

qt_ORB_node_t *qt_new_ORB_node(float x, float y, float x_len, float y_len) {
    qt_ORB_node_t *node = new qt_ORB_node_t;

    node->min_pos.x = x;
    node->min_pos.y = y;
    node->len.x = x_len;
    node->len.y = y_len;

    node->end_node = false;

    node->work_rank = 0;

    node->l = node->r = 0;

    node->tree_vec = new tree_vec_t();

    node->left = NULL;
    node->right = NULL;

    return node;
}

/*
 * free the whole ORB tree
 */
void qt_free_ORB_tree(qt_ORB_node_t *root) {
    if (root == NULL) return;
    if (root->left != NULL) qt_free_ORB_tree(root->left);
    if (root->right != NULL) qt_free_ORB_tree(root->right);

    root->tree_vec->clear();
    if (root->tree_vec != NULL) delete root->tree_vec;
    root->tree_vec = NULL;

    delete root;
}

void qt_print_ORB_tree(qt_ORB_node_t *root, int d, particle_t *ps, int *idx) {
    if (root == NULL) return ;

    // printf("Level: %d:\nmin_pos: %f, %f\nlen:%f, %f\nend_node: %d\nl, r: %d, %d\nwork_rank: %d\n\n",
    //         d, root->min_pos.x, root->min_pos.y, root->len.x, root->len.y,
    //         root->end_node, root->l, root->r, root->work_rank);

    // for (int i = root->l; i <= root->r; i++) {
    //     printf("%f %f\n", ps[idx[i]].pos.x, ps[idx[i]].pos.y);
    // }

    qt_print_ORB_tree(root->left, d+1, ps, idx);
    qt_print_ORB_tree(root->right, d+1, ps, idx);
}

// void qt_test_find_medium(particle_t *ps, int n) {
//     int idx[] = {2, 6, 1, 5, 0, 9, 3, 7, 8, 4};
    
//     n = 5;

//     printf("offset of y: %lu\n", offsetof(vector_t, y));
//     vector_t v = {.x = 1.6f, .y = -2.4f};
//     printf("====== %f\n", *(float *)(((char *)&(v))+4));


//     // float ans = qt_quick_select(ps, idx, 0, 4, offsetof(vector_t, y), (n&1)?(n+1)/2:n/2);

//     // printf("med: %f\n", ans);
//     // for (int i = 0; i < n; i++) {
//     //     printf("%d: %f\n", idx[i], ps[idx[i]].pos.x);
//     // }
// }

void qt_p_construct_BH(particle_t *ps, int *idx, qt_ORB_node_t *node, int rank) {
    if (node == NULL) return ;
    if (node->end_node && node->work_rank == rank) {
        // construct local BH

        // printf("rk: %d, pos: %f, %f, len: %f, %f, v_size: %d\n", rank, node->min_pos.x, node->min_pos.y, node->len.x, node->len.y, node->tree_vec->size());
        int root_node = qt_vec_append(*(node->tree_vec), node->min_pos, node->len);
        // printf("node: %f %f len: %f %f\n", node->min_pos.x, node->min_pos.y, node->len.x, node->len.y);
        // assert(false);

        for (int i = node->l; i <= node->r; i++) {
            // printf("insert id: %d\n", idx[i]);
            qt_insert(ps, idx[i], *(node->tree_vec), root_node);
        }

        // compute mass for the tree
        qt_compute_mass(ps, *(node->tree_vec), root_node);
    } else {
        qt_p_construct_BH(ps, idx, node->left, rank);
        qt_p_construct_BH(ps, idx, node->right, rank);
    }
}

// /******************************/
// /*       Serialization        */
// /******************************/
// void qt_serialize(qt_array_t *a, qt_node_t *root) {
//     int x = 111111;
//     qt_serialize_int(a, &x);

//     printf("size: %d, cap: %d\n", a->size, a->cap);
//     for (int i = 0; i < a->size; i++) {
//         printf("%X ", a->arr[i]);
//     }
//     printf("\n");
// }

// qt_node_t *qt_deserialize(qt_array_t *a) {
// }

// void qt_serialize_int(qt_array_t *a, int *x) {
//     qt_array_reserve(a, sizeof(*x));
//     memcpy(a->arr+a->size, x, sizeof(*x));
//     a->size += sizeof(*x);
// }


// void qt_serialize_float(qt_array_t *a, float *x) {
//     qt_array_reserve(a, sizeof(*x));
//     memcpy(a->arr+a->size, x, sizeof(*x));
//     a->size += sizeof(*x);
// }

// void qt_serialize_vector_t(qt_array_t *a, vector_t * v) {
// }
/******************************/

void qt_p_bcast(qt_ORB_node_t *node, int rank) {
    if (node == NULL) return;

    if (node->end_node) {
        int n = node->tree_vec->size();
        MPI_Bcast(&n, 1, MPI_INT, node->work_rank, MPI_COMM_WORLD);
        node->tree_vec->resize(n);
        MPI_Bcast(node->tree_vec->data(), n, mpi_qt_node_t, node->work_rank, MPI_COMM_WORLD);
    } else {
        qt_p_bcast(node->left, rank);
        qt_p_bcast(node->right, rank);
    }
}

void qt_p_compute_force(qt_ORB_node_t *node, particle_t *ps, int *idx, float dt, float grav, int rank) {
    if (node == NULL) return;
    if (node->end_node && node->work_rank == rank) {
        for (int i = node->l; i <= node->r; i++) {
            vector_t forces = qt_compute_force(ps, idx[i], *(node->tree_vec), 0, grav);
            float acc_x = 0.0f, acc_y = 0.0f;

            particle_t *p = &ps[idx[i]];

            acc_x += forces.x / p->mass;
            acc_y += forces.y / p->mass;

            p->v.x += acc_x * dt;
            p->v.y += acc_y * dt;

            p->pos.x += p->v.x * dt;
            p->pos.y += p->v.y * dt;
        }
    } else {
        qt_p_compute_force(node->right, ps, idx, dt, grav, rank);
        qt_p_compute_force(node->left, ps, idx, dt, grav, rank);
    }
}

void qt_p_gather_particle(qt_ORB_node_t *node, particle_t *ps, int *idx, int rank) {
    if (node == NULL) return;
    if (node->end_node) {
        for (int i = node->l; i <= node->r; i++) {
            MPI_Bcast(&ps[idx[i]], 1, mpi_particle_t, node->work_rank, MPI_COMM_WORLD);
        }
        // if (rank == ROOT_NODE) {
        //     if (node->work_rank != rank) {
        //         for (int i = node->l; i <= node->r; i++) {
        //             // printf("Recv: %d\n", idx[i]);
        //             MPI_Recv(&ps[idx[i]], 1, mpi_particle_t, node->work_rank, idx[i], MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        //         }
        // } else {
        //     if (node->work_rank == rank) {
        //         for (int i = node->l; i <= node->r; i++) {
        //             // printf("Send: %d\n", idx[i]);
        //             MPI_Send(&ps[idx[i]], 1, mpi_particle_t, ROOT_NODE, idx[i], MPI_COMM_WORLD);
        //         }
        //     }
        // }
    } else {
        qt_p_gather_particle(node->left, ps, idx, rank);
        qt_p_gather_particle(node->right, ps, idx, rank);
    }
}