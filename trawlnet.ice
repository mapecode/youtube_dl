// Trawlent 2nd phase: syncing and downloading

module TrawlNet {
  exception DownloadError {
      string reason;
  };

  struct FileInfo {
    string name;
    string hash;
  };

  sequence<FileInfo> FileList;

  interface Downloader {
    FileInfo addDownloadTask(string url)
      throws DownloadError;
  };

  interface Orchestrator {
    FileList getFileList();
    void announce(Orchestrator* other);
    FileInfo downloadTask(string url)
      throws DownloadError;
  };

  interface OrchestratorEvent {
    void hello(Orchestrator* me);
  };

  interface UpdateEvent {
    void newFile(FileInfo file);
  };
};