#include "stdio.h"

int mul(int a, int b) {
    int c = 10;
    int d = c + 25;
    return a * b * d;
}

int add(int a, int b) {
    return a + b + mul(a, b);
}

int main() {
    int a = 100;
    int b = 200;
    int c = add(a, b);
    }