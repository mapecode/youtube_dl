// Trawlent 2nd phase: syncing and downloading

module TrawlNet {
  struct FileInfo {
    string name;
    string hash;
  };

  sequence<FileInfo> FileList;

  interface Downloader {
    FileInfo addDownloadTask(string url);
  };

  interface Orchestrator {
    FileInfo downloadTask(string url);
    FileList getFileList();
    void announce(Orchestrator* other);
  };

  interface OrchestratorEvent {
    void hello(Orchestrator* me);
  };

  interface UpdateEvent {
    void newFile(FileInfo file);
  };
}