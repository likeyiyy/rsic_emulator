#include "stdio.h"

int mul(int a, int b) {
    return a * b;
}

int add(int a, int b) {
    return a + b + mul(a, b);
}

int main() {
    int a = 100;
    int b = 200;
    int c = add(a, b);
    }