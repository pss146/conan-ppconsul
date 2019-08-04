#include <iostream>
#include "ppconsul/status.h"

using ppconsul::Consul;
using namespace ppconsul::status;

int main() {

    // Create a consul client that uses default local endpoint `http://127.0.0.1:8500` and default data center
    Consul consul;

    // We need the status endpoint
    Status status(consul);

    // Determine whether a leader has been elected
    bool isLeaderElected = status.isLeaderElected();

    // Determine the actual raft leader
    auto leader = status.leader();

    // Determine the raft peers
    auto peers = status.peers();

    return 0;
}
