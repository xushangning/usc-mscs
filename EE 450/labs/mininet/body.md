## Abstract

We follow steps in the lab guides with Mininet 2.3.1b1 and iperf3 3.7 on Ubuntu 20.04 and show the results as screenshots in this lab report.

All screenshots in the rest of the report show the state of the screen *after* the given instructions are completed. They are placed in ordered lists whose order corresponds to the order of the steps in the lab guides. For example, the screenshot for "Step 1" is contained in the item numbered "1." in the ordered list. Each screenshot is accompanied by a short text that describes the actions taken and notable deviation from given instructions (if any).

## Lab 1: Introduction to Mininet

### 2 Invoking Mininet using the CLI

#### 2.1 Invoking Mininet using the default topology

1. A Linux terminal was launched.
    ![](imgs/1/2/1/1.png)
2. Mininet with a minimal topology was started.
    ![](imgs/1/2/1/2.png)
3. Executed the `help` command.
    ![](imgs/1/2/1/3.png)
4. Executed the `nodes` command.
    ![](imgs/1/2/1/4.png)
5. Executed the `net` command.
    ![](imgs/1/2/1/5.png)
6. Executed `ifconfig` on host h1 with `h1 ifconfig`.
    ![](imgs/1/2/1/6.png)

#### 2.2 Testing connectivity

1. Pinged host h2.
    ![](imgs/1/2/2/1.png)
2. Stopped the emulation with `exit`.
    ![](imgs/1/2/2/2.png)

### 3 Building and emulating a network in Mininet using the GUI

#### 3.1 Building the network topology

1. Launched MiniEdit.
    ![](imgs/1/3/1/1.png)
2. Built the topology in the lab guide.
    ![](imgs/1/3/1/2.png)
3. Configured the IP addresses of host h1 and h2.
    ![](imgs/1/3/1/3.png)

#### 3.2 Testing connectivity

1. The emulation was started after the "Run" button was clicked.
    ![](imgs/1/3/2/1.png)
2. Opened host h1 and h2's terminals
    ![](imgs/1/3/2/2.png)
3. Executed `ifconfig` on h1 and h2's terminals.
    ![](imgs/1/3/2/3.png)
4. Pinged host h2 from h1.
    ![](imgs/1/3/2/4.png)
5. The emulation was stopped.
    ![](imgs/1/3/2/5.png)

#### 3.3 Automatic assignment of IP addresses

1. Manually assigned addresses in previous steps were removed.
    ![](imgs/1/3/3/1.png)
2. The default IP base was changed in the "Preferences" window.
    ![](imgs/1/3/3/2.png)
3. The emulation was started.
    ![](imgs/1/3/3/3.png)
4. h1's terminal was opened.
    ![](imgs/1/3/3/4.png)
5. `ifconfig` was executed on h1 and h2's terminals, whose output showed that the IP base had indeed changed.
    ![](imgs/1/3/3/5.png)
6. The emulation was stopped.
    ![](imgs/1/3/3/6.png)

#### 3.4 Saving and loading a Mininet topology

1. The network topology was saved to the file ee450.mn
    ![](imgs/1/3/4/1.png)
2. The topology saved in the previous step was loaded.
    ![](imgs/2/2/2.png)

## Lab 2

### 2 Lab topology

1. Launched MiniEdit.
    ![](imgs/2/2/1.png)
2. The network topology saved in Lab 1 was loaded.
    ![](imgs/2/2/2.png)
3. Emulation was started.
    ![](imgs/2/2/3.png)

#### 2.1 Starting host h1 and host h2

1. Launched host h1's terminal.
    ![](imgs/2/2/1/1.png)
2. Pinged h2 from h1 to test connectivity.
    ![](imgs/2/2/1/2.png)

### 3 Using iPerf3 (client and server commands)

#### 3.1 Starting client and server

1. Launched h2's terminal.
    ![](imgs/2/3/1/1.png)
2. Launched `iperf3` in server mode in h2's terminal.
    ![](imgs/2/3/1/2.png)
3. Launched `iperf3` in client mode in h1's terminal.
    ![](imgs/2/3/1/3.png)
4. The server in h2's terminal was stopped.
    ![](imgs/2/3/1/4.png)

#### 3.2 Setting transmitting time period

1. The `iperf3` server was started on h2.
    ![](imgs/2/3/2/1.png)
2. The `iperf3` client was started with the `-t 5` option.
    ![](imgs/2/3/2/2.png)
3. The server in h2's terminal was stopped.
    ![](imgs/2/3/2/3.png)

#### 3.3 Setting time interval

1. The server was started on h2 with a time interval.
    ![](imgs/2/3/3/1.png)
2. The client was started on h1 with a time interval.
    ![](imgs/2/3/3/2.png)
3. The server in h2's terminal was stopped.
    ![](imgs/2/3/3/3.png)

#### 3.4 Changing the number of bytes to transmit

1. The server was started on h2.
    ![](imgs/2/3/4/1.png)
2. The client was started on h1 with a specified number of bytes to transmit.
    ![](imgs/2/3/4/2.png)
3. The server in h2's terminal was stopped.
    ![](imgs/2/3/4/3.png)

#### 3.5 Specifying the transport-layer protocol

1. The server was started on h2.
    ![](imgs/2/3/5/1.png)
2. The client was started on h1 with UDP as the transport-layer protocol.
    ![](imgs/2/3/5/2.png)
3. The server in h2's terminal was stopped.
    ![](imgs/2/3/5/3.png)

#### 3.6 Changing port number

1. The server was started on h2 with the listening port set to 3250.
    ![](imgs/2/3/6/1.png)
2. The client was started on h1 and was told to connect to 3250.
    ![](imgs/2/3/6/2.png)
3. The server in h2's terminal was stopped.
    ![](imgs/2/3/6/3.png)

#### 3.7 Export results to JSON file

1. The server was started on h2.
    ![](imgs/2/3/7/1.png)
2. The client was started twice on h1 with the output format set to JSON. For the first time the client output to stdout and to test_results.json for the second time.
    ![](imgs/2/3/7/2.png)
3. The server in h2's terminal was stopped.
    ![](imgs/2/3/7/3.png)

#### 3.8 Handle one client

1. The server was started on h2 and was told to accept only one client.
    ![](imgs/2/3/8/1.png)
2. The client was started on h1.
    ![](imgs/2/3/8/2.png)

### 4 Plotting iPerf3 results

1. The server was started on h2.
    ![](imgs/2/4/1.png)
2. The client was started on h1 with output format set to JSON and output redirected to test_results.json.
    ![](imgs/2/4/2.png)
3. Output files for `iperf3` were generated by the plotting script.
    ![](imgs/2/4/3.png)
4. Entered the results folder.
    ![](imgs/2/4/4.png)
5. Tried to open throughput.pdf with `xdg-open` but failed, because Firefox, which could not run under root, was selected by `xdg-open` to open the PDF file. We manually opened throughput.pdf with Evince, the default document viewer on our system. All figures produced by the plotting script were placed at the end of this section.
    ![](imgs/2/4/5.png)
6. The server in h2's terminal was stopped.
    ![](imgs/2/4/6.png)

The following figures were produced by the plotting script:

- bytes.pdf<br>
    ![](imgs/2/4/bytes.png)
- cwnd.pdf<br>
    ![](imgs/2/4/cwnd.png)
- MTU.pdf<br>
    ![](imgs/2/4/MTU.png)
- retransmits.pdf<br>
    ![](imgs/2/4/retransmits.png)
- RTT_Var.pdf<br>
    ![](imgs/2/4/RTT_Var.png)
- RTT.pdf<br>
    ![](imgs/2/4/RTT.png)
- throughput.pdf<br>
    ![](imgs/2/4/throughput.png)

## Conclusion

The lab went as expected. The MiniEdit GUI is difficult to use because it lacks some common GUI operations. For example, there is no way to close the right-click menu and the "Host Option" item in the right-click menu doesn't work at all.
