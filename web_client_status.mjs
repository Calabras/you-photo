export class StatusPollerJS {
  constructor(backendApi, statusView, pollIntervalMs = 5000) {
    this.backendApi = backendApi;
    this.statusView = statusView;
    this.pollIntervalMs = pollIntervalMs;
    this.activeTimerId = null;
  }

  startPolling(orderId) {
    throw new Error("Not implemented");
  }

  stopPolling() {
    throw new Error("Not implemented");
  }

  receiveStatus(orderStatus, history) {
    throw new Error("Not implemented");
  }

  receiveError(error) {
    throw new Error("Not implemented");
  }
}

export class OrderStatusView {
  constructor(statusElement, historyElement, errorElement) {
    this.statusElement = statusElement;
    this.historyElement = historyElement;
    this.errorElement = errorElement;
  }

  renderStatus(orderStatus, history) {
    throw new Error("Not implemented");
  }

  renderError(error) {
    throw new Error("Not implemented");
  }
}
