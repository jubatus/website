
Server Generation Using Code Generator
--------------------------------------

In Jubatus, algorithms like machine learning tasks are realized as plugins so that we can add algorithms easily.
But in the current implementation it is found to be difficult for users to do implement new algorithm.

First, under current design, we must write same definition many times everytime we add new learning algorithm.
When we add recommender to published implementation, we had to define RPC interface of recommender into six points, that is, header and implementation of client, header and implementation of Jubakeeper and header and implementation of server.
Furthermore, we found that we must repeat writing registration to server (such as MPRPC_GEN and MPRPC_PROC in pficommon) seven times.
This is a "hotbed" of bugs because every time we change the API, we must correct every definition.

Next, because a lot of macros and templates are used in Jubatus, compile errors are complicated. Therefore, it is necessary for developer to deeply know about Jubatus in order to implement machine learning tasks in Jubatus.

Such difficulties are not appropriate if Jubatus aims for a distributed machine learning framework.

.. Jubatusは機械学習などのアルゴリズムをプラグイン化し，容易に追加できることを目的にしているが，公開されている実装に対してrecommenderを追加しようとした場合，それぞれのRPCインターフェースをクライアントのヘッダと実装，Jubakeeperのヘッダと実装，サーバー本体のヘッダと実装の6箇所に定義する必要があった．さらにpficommonのMPRPC_GEN, MPRPC_PROC等，サーバーへの関数登録などで合計7箇所に記述を繰り返す必要があることが明らかになった．このような設計では，新しい学習アルゴリズムを追加する度に同じRPC定義を7回繰り替えさなければならず，APIの仕様を変更するたびに同じような修正を繰り返さなくてはならないためバグが入り込む温床となっており，機械学習を分散環境で実装するためのフレームワークとして容易に追加できると言いがたい．さらに，C++のマクロおよびテンプレートを多用しているため，コンパイルエラーが複雑なものとなり，Jubatusを用いて機械学習を実装するにはJubatusの深い知識が必要となっていた．

We checked we can create system through the following procedure : 

.. 結果として

#. Define RPC interfaces that server should have.
#. Generate codes of IDL, server, Jubakeeper with generator. 
#. Implement codes of interface of user-defined class and (if necessary, ) mix operation for each RPC. 
#. Generate clients with msgpack-idl

.. #. サーバーが持つべきRPCインターフェースを定義する
.. #. ジェネレータによりIDL, サーバー，Jubakeeperのコードを生成
.. #. RPC毎にサーバーが利用するユーザ定義クラスのインターフェースの実体，および必要に応じてmix操作を作成
.. #. msgpack-idlを用いてクライアントを生成

Owing to this procedure, definition of RPC reduces from seven to three.
We also checked we can create recommener, classifier, regression, and stat.

.. という手順で一連のシステムを作成することができることを確認した．実際にRPC定義をするのは，7箇所から3箇所に削減された．これを用いて，recommender, classifier, regression, statが構成出来ることを確認した．


Generator
~~~~~~~~~

We define interface with `MsgPack-IDL <https://github.com/msgpack/msgpack-haskell/blob/master/msgpack-idl/Specification.md>`_ .
So please read the instruction of MsgPack-IDL first.
Aside from MsgPack-IDL's original syntax, we must add annotations for each method of RPC service in order to generate codes used in Jubatus.
Annotations are interpreted by the code generator, but they are ignored as comments by MsgPack-IDL.
Therefore, we can generate each clients with same annotated method by MsgPack-IDL.

.. `MsgPack-IDL <https://github.com/msgpack/msgpack-haskell/blob/master/msgpack-idl/Specification.md>`_ によりインターフェースを定義する．ただし，そのままJubatusのコードを生成するためにはRPCサービスの各メソッドにアノテーションをつける必要がある．これはコードジェネレータでは解釈されるが，MsgPack-IDLではコメントとして無視されるため，同じファイルで各種クライアントも生成できる．


- Declaration of Annotated Class Method.

  - First annotation defines routing of request. This annotation should begin with "#@" and be followed with one of "cht", "broadcast" and "random". Each keyword represents distribution of request with Consistent Hashing, broadcast of request to all servers, and sending of request to a randomly chosen server, respectively. We can cover distribute methods used in typical machine learning tasks.

    - Method annotated with "cht" must have two arguments. First is a string used as a key of cht. Second argument for users of this method.
    - Method annotated with "broadcast" or "random" must have one argument and one return value. void type is not available. If argument or return value is not needed, we must add meaningless value such as value of int type.

  - Second annotation defines read/write of request. If we choose "analysis", data is locked in server side with read lock and is accesible by multiple thread simultaneously. On the other hand, if we choose "update", data is locked with write lock. Therefore, we can safely update data.

  - Third annotation defines how to aggrate the result of API call. Available aggregator is written in src/framework/aggregators.hpp.


.. - アノテーションつきクラスメソッドの宣言

..   - 一番目のアノテーションでは，リクエストのルーティングを宣言することができる．必ず "#@" から始まり， "cht", "broadcast", "random" のいずれかを表す．それぞれ，Consistent Hashingによるリクエストの分散，全サーバーへリクエストをブロードキャスト，ランダムに選択されたいずれかのサーバーへリクエストを送信，を表す．これによって，典型的だと思われる機械学習の分散方式をカバーすることができる．

..     - chtアノテーションがあるメソッドは，第一引数がchtのキーとなるstring, 第二引数をユーザ利用の引数としなければならない．
..     - broadcast, randomアノテーションがあるメソッドは，必ずひとつの引数とひとつの返り値をもたなければならない．void型は利用できない．引数や返り値が必要ない場合は，意味のないintなどを指定しておくこと．

..   - 二番目のアノテーションでは，リクエストのread/writeを宣言することができる．analysisにするとサーバー側でreadロックされることになり，複数のスレッドからの同時アクセスが可能となる．updateにするとサーバー側でwriteロックされることになり，安全にデータを更新することができる．

..   - 三番目のアノテーションでは，API呼び出しの結果のアグリゲーションを定義することができる．利用可能なアグリゲータはソースのsrc/framework/aggregators.hppに掲載されている．


.. code-block:: java

   message somemsgtype {
     1: string key;
     2: string value;
     3: int version;
   };

  service kvs {

    #@cht #@update #@all_and
    int put(string key, string value);

    #@cht #@analysis #@random
    somemsgtype get(string key, int v);

    #@cht #@update #@all_and
    int del(string key, int v);

    #@broadcast #@update #@all_and
    int clear(int);

    #@broadcase #@analysis #@merge
    map<string, string> get_status(int);
  };

We need Ocaml and Omake to build the generator . Suppose the name of this file is kvs.idl. We can generate codes in the following manner.

.. generatorのビルドにはOCamlおよびOMakeが必要である．このファイルをkvs.idlとすると，

::

  jubatus $ cd tools/generator
  jubatus $ omake
  jubatus $ ./jenerator path/to/kvs.idl -o .
  jubatus $ ls kvs*
  kvs_impl.cpp kvs_keeper.cpp

Two file will be generated. If we add -t option, we can generate additionally C++ source file which is template of implementation of server.
At that time generator will automatically add APIs named save/load.


.. 通常は2つのファイルが生成される．-tオプションをつければ，サーバー実装の雛形となるC++のソースファイルが生成される．このとき，ジェネレータはsave/loadというAPIを自動で追加する．

TODO: how to implement mix

.. これは，jubatus_serv<M, Diff>のM->saveを呼び出す．これによって，ユーザはsave/loadに関するサーバーの実装を書かなくてよくなり，機械学習のデータMのsave/load（シリアライゼーション）を実装するだけでよい．

.. IDLを用いたクライアントの生成は

Server
~~~~~~

MsgPack-IDL generates headers for mprpc of pficommon. In the example above, the name of the header should be kvs_server.hpp.
These headers register functors of RPC definition to servers.
This registration is executed by passing the class name to class server with CRTP (Compressed Real Time Protocol).
Generated kvx_impl.cpp construct server with kvs_server.hpp.
Generators defines kvs_serv class in kvs_impl.cpp.
Users should declare and implement this class under the same namespace.
By this process, users can insert server-side implementation to the framework.
At this time, API named get_diff and putdiff are added to server automatically.
It is only implementing get_diff, put_diff and reduce in server that users must do in order to use mix operation in a distributed environment.

Here is the explanation of kvs_serv class

.. msgpack-idlが生成するpficommonのmprpc向けヘッダは，CRTPによりクラス名を渡すことにより，RPC定義のファンクタをサーバーに登録する．ジェネレータが生成するkvs_impl.cppは，そのkvs_server.hppを利用してサーバーを構成する．ジェネレータはkvs_impl.cppの中でkvs_servというクラスを指定する．ユーザは同じ名前空間でこれを宣言・実装することによって，サーバー側の実装をフレームワークに組み込むことができる．このとき，サーバーは自動的にget_diff, put_diffというAPIをサーバーに追加する．これにより，サーバーでは，Mにget_diff, put_diffおよびreduceを実装するだけで分散環境でのmixを利用できる．以下に例を示す．

.. code-block:: cpp

  namespace jubatus { namespace server {
  class kvs_serv : jubatus_serv<my_kvs, diff_t> {
  public:
    kvs_serv(const server_argv&);
    virtual ~kvs_serv();
    
    static diffv get_diff(const my_kvs*);
    static int put_diff(my_kvs*, diff_t);
    static int reduce(const my_kvs*, const diff_t&, diff_t&);

    pfi::lang::shared_ptr<my_kvs> make_model();
    void after_laod();

    int put(string key, string value);
    somemsgtype get(string key, int v);
    int del(string key, int v);
    int clear(int);
    map<string, string> get_status(int);
  };
  }}

Users must implement make_model() and define initialization of constructor M(my_kvs).
Also, users can implement after_load(). It modify the state of server after initialization.
For example of classifier, users can execute set_mixer and modify the algorithm of mix.
Users can use get_diff, put_diff and reduce are available by registering functors of them.
Registration is done with jubatus_serv<M, Diff>::set_mixer().

.. ユーザーは，make_model()を実装し，M(my_kvs)の初期化処理を定義しなければならない．また，after_load()を実装し，初期化後のサーバーの状態を変更することができる．例えば，classifierであれば，ここでset_mixerを実行することにより，mixのアルゴリズムを変更することができる．get_diff, put_diff, reduceはjubatus_serv<M,Diff>::set_mixer()を用いてファンクタを設定することにより利用できる．

In the previous example, template parameter M is set to be my_kvs.
Users must implement the following APIs in my_kvs.

.. この例ではMをmy_kvsとしている．my_kvsが実装していなければならないAPIは以下のとおりである．

.. cpp:function:: bool my_kvs::save(ostream&)


.. cpp:function:: bool my_kvs::load(istream&)


main() is implemented in kvs_impl.cpp. Therefore, users don't have to implement main function.
Command line options are same among servers.
The options can be referenced with -? option.

.. kvs_impl.cppの中ではmain関数も実装されており，ユーザはmainを実装する必要はない．コマンドライン引数の仕様は統一されており，-?で参照することができる．

Keeper
~~~~~~

Users don't have to implement nothing regarding keeper.
Users have only to compile source codes of keeper.
As the generator generate kvs_keeper.cpp, compile it and users can get keeper program.
kvs_keeper.cpp has only main function.
In this main function, keeper mainly does two things.
First, keeper specifies routing of cht, broadcast and random, update process, and read process.
These are defined in the annotated idl file.
Second, keeper register proxy functor for each RPC.

.. ユーザーはkeeperに関して何らかの実装をする必要はなく，ただコンパイルすればよい．ジェネレータがkvs_keeper.cppを生成するので，それをコンパイルすればkeeperとなる．実体はmain関数の実装があるだけで，broadcast, random, chtのルーティング，および更新処理と読込処理を指定して各RPCのプロキシとなるファンクタを登録する．

- cht

  - Specifies servers with Consistent Hashing and key used in hashing. This process guarantees that requests with same key is send to same servers. Currently request is send to two servers because of redundancy. As this is senchronous call of MPRPC, all RPC call are serialized. Therefore, process time is proportional to the number of servers.

- broadcast

  - Send request to all servers. As this is senchronous call of MPRPC, all RPC call are serialized. Therefore, process time is proportional to the number of servers.

- random

  - Send request to randomly chosen server among all servers.

.. - broadcast
..  - 全サーバーにリクエストを送信する．MPRPCが同期呼び出しであるため，全てのRPC呼び出しがシリアルに実行されるため，処理時間はサーバーの台数分だけかかる．
.. - random
..   - 全サーバーの中から，ランダムにサーバーを選択しリクエストを送信する．
.. - cht
..   - キーを指定することによって，Consistent Hashingを用いて同じキーは同じサーバーに必ず送信されることを保証する．現在は冗長化のために，2台にリクエストを送信している．MPRPCが同期呼び出しであるため，2回のRPC呼び出しがシリアルに実行される．


Future works
~~~~~~~~~~~~

Limit in Number of Simultaneous Connection
.................................................

In the current I/O architecture of pficommon, we cannot maintain as many simultaneous connections as threads.
Therefore, it is necessary to establish and disconnect connections frequently.
This switching is a bottleneck especially for Jubakepper.
One possible solution is to prepare caching mechanism of connection in Jubakeeper.
But as connection number reaches to the limit of simultaneous connection in server-side, the lifecycle of TCP connection gets complicated.
Alternative choice is to use or create servers with asynchronous I/O like epoll, instead of accepted-based MsgPack-RPC servers.
Public MsgPack servers have asynchronous I/O.
But it is difficult to use it, partially because implementation of asynchronous I/O is not maintained.

.. 現状のpficommonのI/Oアーキテクチャでは，スレッド数と同数の同時接続しか維持できない．従ってコネクションの接続と切断の繰り返しが必要になり，特にJubakeeperでボトルネックとなる．仮にJubakeeperでコネクションのキャッシュ機構を用意した場合，サーバー側での同時接続数に限界がくると同時にTCPコネクションのライフサイクルが複雑になる．代替案として acceptベースのMsgpack-RPCサーバーではなく，epollなどの非同期I/Oを用いたサーバーを利用または作成する．公式のMsgpackサーバーは非同期I/Oの機能を持っているがメンテナンスがされてないこともあり利用しにくい．pficommonのMPRPCサーバーを改造するという選択肢がある．

.. #. acceptベースのMsgpack-RPCサーバーではなく，epollなどの非同期I/Oを用いたサーバーを利用または作成する．公式のMsgpackサーバーは非同期I/Oの機能を持っているがメンテナンスがされてないこともあり利用しにくい．pficommonのMPRPCサーバーを改造するという選択肢がある．

.. #. Jubatusのメッセージングアーキテクチャを根本から見直す．ブロードキャスト，ランダム，RR，CHTなどの複数のプロトコルとZooKeeperの死活監視を統合したメッセージング機構を実装しなおす．


A Proglem with broadcast-type API
..........................................

In the current implementation, it is Jubakeeper that executes broadcast in APIs which send RPC request to all servers.
But in such a  broadcast-type RPC, sender cannot satisfies requirement of APIs if it simply sends request to all servers.
Because it depends on APIs how to aggregate results from each servers.
For example, "set_config" of classifier must be repeated until results of `all` servers are `success` (config is successfully set or server gets stopped).
On the other hand, in those APIs that acquire status such as "get_status", we need to `united all successfull return values to a single map`.
Current generator cannot make out such a requirement.

.. 全サーバーに対してRPCを実行するタイプのAPIでの実際のブロードキャストは，現在Jubakeeperが行なっている．しかし，ブロードキャスト型のRPCでは，各サーバーから得られた結果のまとめ方（アグリゲート）がAPIによって要件が異なるため，単純に全員に送信するだけでは要求を満たせない場合がある．たとえば，classifierなどのset_configは全サーバーでの実行結果が `全て成功` になるまで繰り返す必要がある（成功するか，サーバーが停止するかのどちらかでなければならない）一方で，get_statusのような状態取得APIを考えた場合には， `成功した返り値どうしをひとつのmapに結合する` といった動作が必要になる．これらの記述は，いまのジェネレータでは上手く読み出すことができない．


Interface and Description of Processing
..............................................

Developer of machine learning tasks must consider how to unite multiple lerners or how to separate feature extractors and learners.
But it is not trivial for developer where and how to implement to achieve this objectives.

Furthermore, current generator can describe only interface of learners.
There is no method for developer to consider algorithm of machine learning transparently.
It is benefitical that developers to experiment or make trial and error regardless of the configuration of underlying architecture of machines (single server or multiple servers).
It is worth considering to develop abstract languages for describing algorithms.

.. 複数の機械学習を結合したり，特徴量変換と学習器本体を分離するためには，C++を単純に記述していくインターフェースではどこをどうしてよいかが開発者にとって自明でない．現状のジェネレータでは学習器のインターフェースしか記述することができない．アルゴリズム自体も抽象化された言語上で試行錯誤し，機械学習を実装するユーザが一台のマシン上でも，複数台のマシン上でも透過的に実行や試行錯誤ができるような機能を，検討する必要がある．
