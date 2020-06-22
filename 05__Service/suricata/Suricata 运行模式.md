

## 基本组成：

是由所谓的线程（threads）、线程模块 （thread-modules）和队列（queues）组成。Suricata是一个多线程的程序，因此在同一时刻会有多个线程在工作。线程模块是依据 功能来划分的，比如一个模块用于解析数据包，另一个模块用于检测数据包等。每个数据包可能会有多个不同的线程进行处理，队列就是用于将数据包从一个线程传 递到另一个线程。与此同时，一个线程可以拥有多个线程模块，但是在某一时刻只有一个模块在运行





``` 
------------------------------------- Runmodes ------------------------------------------
| RunMode Type      | Custom Mode       | Description
|----------------------------------------------------------------------------------------
| PCAP_DEV          | single            | Single threaded pcap live mode
|                   ---------------------------------------------------------------------
|                   | autofp            | Multi threaded pcap live mode.  Packets from each flow are assigned to a single detect thread, unlike "pcap_live_auto" where packets from the same flow can be processed by any detect thread
|                   ---------------------------------------------------------------------
|                   | workers           | Workers pcap live mode, each thread does all tasks from acquisition to logging
|----------------------------------------------------------------------------------------
| PCAP_FILE         | single            | Single threaded pcap file mode
|                   ---------------------------------------------------------------------
|                   | autofp            | Multi threaded pcap file mode.  Packets from each flow are assigned to a single detect thread, unlike "pcap-file-auto" where packets from the same flow can be processed by any detect thread
|----------------------------------------------------------------------------------------
| PFRING(DISABLED)  | autofp            | Multi threaded pfring mode.  Packets from each flow are assigned to a single detect thread, unlike "pfring_auto" where packets from the same flow can be processed by any detect thread
|                   ---------------------------------------------------------------------
|                   | single            | Single threaded pfring mode
|                   ---------------------------------------------------------------------
|                   | workers           | Workers pfring mode, each thread does all tasks from acquisition to logging
|----------------------------------------------------------------------------------------
| NFQ               | autofp            | Multi threaded NFQ IPS mode with respect to flow
|                   ---------------------------------------------------------------------
|                   | workers           | Multi queue NFQ IPS mode with one thread per queue
|----------------------------------------------------------------------------------------
| NFLOG             | autofp            | Multi threaded nflog mode
|                   ---------------------------------------------------------------------
|                   | single            | Single threaded nflog mode
|                   ---------------------------------------------------------------------
|                   | workers           | Workers nflog mode
|----------------------------------------------------------------------------------------
| IPFW              | autofp            | Multi threaded IPFW IPS mode with respect to flow
|                   ---------------------------------------------------------------------
|                   | workers           | Multi queue IPFW IPS mode with one thread per queue
|----------------------------------------------------------------------------------------
| ERF_FILE          | single            | Single threaded ERF file mode
|                   ---------------------------------------------------------------------
|                   | autofp            | Multi threaded ERF file mode.  Packets from each flow are assigned to a single detect thread
|----------------------------------------------------------------------------------------
| ERF_DAG           | autofp            | Multi threaded DAG mode.  Packets from each flow are assigned to a single detect thread, unlike "dag_auto" where packets from the same flow can be processed by any detect thread
|                   ---------------------------------------------------------------------
|                   | single            | Singled threaded DAG mode
|                   ---------------------------------------------------------------------
|                   | workers           | Workers DAG mode, each thread does all  tasks from acquisition to logging
|----------------------------------------------------------------------------------------
| AF_PACKET_DEV     | single            | Single threaded af-packet mode
|                   ---------------------------------------------------------------------
|                   | workers           | Workers af-packet mode, each thread does all tasks from acquisition to logging
|                   ---------------------------------------------------------------------
|                   | autofp            | Multi socket AF_PACKET mode.  Packets from each flow are assigned to a single detect thread.
|----------------------------------------------------------------------------------------
| NETMAP(DISABLED)  | single            | Single threaded netmap mode
|                   ---------------------------------------------------------------------
|                   | workers           | Workers netmap mode, each thread does all tasks from acquisition to logging
|                   ---------------------------------------------------------------------
|                   | autofp            | Multi threaded netmap mode.  Packets from each flow are assigned to a single detect thread.
|----------------------------------------------------------------------------------------
| UNIX_SOCKET       | single            | Unix socket mode
|                   ---------------------------------------------------------------------
|                   | autofp            | Unix socket mode
|----------------------------------------------------------------------------------------
| WINDIVERT(DISABLED) | autofp            | Multi-threaded WinDivert IPS mode load-balanced by flow
|----------------------------------------------------------------------------------------

```

所有运行模式都有一个名称：single、workers、autofp。