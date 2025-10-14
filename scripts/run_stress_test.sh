#!/bin/bash

# RAI Toolkit Stress Test Runner
# Orchestrates Streamlit app startup, Playwright test execution, and report generation

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
APP_PATH="$PROJECT_ROOT/project1_risk_framework/app.py"
PORT=${STREAMLIT_PORT:-8501}
STREAMLIT_PID=""

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to cleanup Streamlit process on exit
cleanup() {
    if [ -n "$STREAMLIT_PID" ]; then
        print_info "Stopping Streamlit (PID: $STREAMLIT_PID)..."
        kill $STREAMLIT_PID 2>/dev/null || true
        wait $STREAMLIT_PID 2>/dev/null || true
        print_success "Streamlit stopped"
    fi
}

# Register cleanup function
trap cleanup EXIT INT TERM

# Function to find available port
find_available_port() {
    while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
        print_warning "Port $PORT is in use, trying next port..."
        PORT=$((PORT + 1))
    done
    echo $PORT
}

# Function to wait for app to be ready
wait_for_app() {
    local max_attempts=30
    local attempt=1
    
    print_info "Waiting for Streamlit app to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "http://localhost:$PORT" > /dev/null 2>&1; then
            print_success "Streamlit app is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_error "Streamlit app failed to start within 30 seconds"
    return 1
}

# Main execution
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║     RAI Toolkit Stress Test Suite                    ║"
    echo "║     Senior Governance Professional Perspective       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    # Check prerequisites
    print_info "Checking prerequisites..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "python3 not found. Please install Python 3.11+"
        exit 1
    fi
    
    if ! command -v streamlit &> /dev/null; then
        if ! python3 -m streamlit --version &> /dev/null; then
            print_error "Streamlit not found. Install with: pip install streamlit"
            exit 1
        fi
        STREAMLIT_CMD="python3 -m streamlit"
    else
        STREAMLIT_CMD="streamlit"
    fi
    
    # Check if stress test dependencies are installed
    if ! python3 -c "import playwright" 2>/dev/null; then
        print_warning "Playwright not found. Installing stress test dependencies..."
        pip install -r "$PROJECT_ROOT/requirements-stress.txt"
        python3 -m playwright install chromium
    fi
    
    # Find available port
    PORT=$(find_available_port)
    print_info "Using port: $PORT"
    
    # Start Streamlit in background
    print_info "Starting Streamlit app..."
    $STREAMLIT_CMD run "$APP_PATH" \
        --server.port=$PORT \
        --server.headless=true \
        --server.fileWatcherType=none \
        --browser.gatherUsageStats=false \
        > "$PROJECT_ROOT/streamlit.log" 2>&1 &
    
    STREAMLIT_PID=$!
    print_success "Streamlit started (PID: $STREAMLIT_PID)"
    
    # Wait for app to be ready
    if ! wait_for_app; then
        print_error "Failed to start app. Check streamlit.log for details"
        cat "$PROJECT_ROOT/streamlit.log"
        exit 1
    fi
    
    # Run Playwright tests
    echo ""
    print_info "Running comprehensive stress tests..."
    echo ""
    
    cd "$PROJECT_ROOT"
    
    # Set base URL for tests
    export STRESS_TEST_URL="http://localhost:$PORT"
    
    # Run pytest with Playwright
    if pytest tests/stress_agent.py \
        --base-url="$STRESS_TEST_URL" \
        --browser=chromium \
        --headed=false \
        --screenshot=only-on-failure \
        --video=retain-on-failure \
        -v \
        --tb=short; then
        
        echo ""
        print_success "All stress tests completed successfully!"
    else
        echo ""
        print_warning "Some tests failed. Check the report for details."
    fi
    
    # Report location
    echo ""
    print_info "Test execution complete."
    
    LATEST_REPORT=$(ls -t "$PROJECT_ROOT/stress_test_reports"/report_*.html 2>/dev/null | head -n1)
    
    if [ -n "$LATEST_REPORT" ]; then
        print_success "Report generated: $LATEST_REPORT"
        
        # Try to open report in browser
        if command -v open &> /dev/null; then
            print_info "Opening report in browser..."
            open "$LATEST_REPORT"
        elif command -v xdg-open &> /dev/null; then
            print_info "Opening report in browser..."
            xdg-open "$LATEST_REPORT"
        else
            print_info "To view report, open: $LATEST_REPORT"
        fi
    else
        print_warning "No report found. Check test output for errors."
    fi
    
    echo ""
    print_success "Stress test suite complete!"
    echo ""
}

# Run main function
main "$@"

