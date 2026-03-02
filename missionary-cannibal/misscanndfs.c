#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    int left[2];
    int right[2];
    int boat;
} State;

bool visited[4][4][4][4][2];
State path[100];
int pathIndex = 0;
bool found = false;

bool isValid(State s) {
    if(s.left[0] < 0 || s.left[1] < 0 || s.right[0] < 0 || s.right[1] < 0) return false;
    if(s.left[0] > 3 || s.left[1] > 3 || s.right[0] > 3 || s.right[1] > 3) return false;
    if((s.left[0] > 0 && s.left[0] < s.left[1]) || (s.right[0] > 0 && s.right[0] < s.right[1])) return false;
    return true;
}

bool isVisited(State s) {
    return visited[s.left[0]][s.left[1]][s.right[0]][s.right[1]][s.boat];
}

void markVisited(State s) {
    visited[s.left[0]][s.left[1]][s.right[0]][s.right[1]][s.boat] = true;
}

bool isDone(State s) {
    return (s.right[0] == 3 && s.right[1] == 3);
}

State makeMove(State s, int m, int c) {
    State newState = s;
    if(s.boat == 0) { 
        newState.left[0] -= m;
        newState.left[1] -= c;
        newState.right[0] += m;
        newState.right[1] += c;
        newState.boat = 1;
    } else { 
        newState.right[0] -= m;
        newState.right[1] -= c;
        newState.left[0] += m;
        newState.left[1] += c;
        newState.boat = 0;
    }
    return newState;
}

void printState(State s) {
    printf("Left: M=%d C=%d  Right: M=%d C=%d  Boat: %s\n",
           s.left[0], s.left[1], s.right[0], s.right[1],
           s.boat == 0 ? "Left" : "Right");
}

void printSolution() {
    for(int i = 0; i < pathIndex; i++) {
        printf("Step %d: ", i);
        printState(path[i]);
    }
}

void dfs(State current) {
    if(found) return;
    path[pathIndex++] = current;
    markVisited(current);
    if(isDone(current)) {
        printSolution();
        found = true;
        return;
    }
    int moves[5][2] = {{1,0}, {2,0}, {0,1}, {0,2}, {1,1}};
    for(int i = 0; i < 5; i++) {
        State next = makeMove(current, moves[i][0], moves[i][1]);
        if(isValid(next) && !isVisited(next)) {
            dfs(next);
        }
    }
    pathIndex--;  
}

int main() {
    State initial = {{3, 3}, {0, 0}, 0};
    memset(visited, false, sizeof(visited));
    printf("Initial State:\n");
    printState(initial);
    dfs(initial);
    if(!found) {
        printf("No solution\n");
    }
    return 0;
}