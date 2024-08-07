:orphan:

.. _errors:

==============
Error Messages
==============

.. This section lists descriptions and background for common error messages and warnings raised or emitted by SQLAlchemy.

この項では、SQLAlchemyによって生成または出力される一般的なエラーメッセージと警告の説明とバックグラウンドを示します。

.. SQLAlchemy normally raises errors within the context of a SQLAlchemy-specific exception class. For details on these classes, see :ref:`core_exceptions_toplevel` and :ref:`orm_exceptions_toplevel`.

SQLAlchemyは通常、SQLAlchemy固有の例外クラスのコンテキスト内でエラーを発生させます。これらのクラスの詳細については、 :ref:`core_exceptions_toplevel` および :ref:`orm_exceptions_toplevel` を参照してください。

.. SQLAlchemy errors can roughly be separated into two categories, the **programming-time error** and the **runtime error**.     Programming-time errors are raised as a result of functions or methods being called with incorrect arguments, or from other configuration-oriented methods such  as mapper configurations that can't be resolved. The programming-time error is typically immediate and deterministic. The runtime error on the other hand represents a failure that occurs as a program runs in response to some condition that occurs arbitrarily, such as database connections being exhausted or some data-related issue occurring. Runtime errors are more likely to be seen in the logs of a running application as the program encounters these states in response to load and data being encountered.

SQLAlchemyエラーは、 **プログラミング時エラー** と **実行時エラー** の2つのカテゴリに大別できます。プログラミング時エラーは、関数またはメソッドが不正な引数で呼び出された結果、または解決できないマッパー構成などの他の構成指向のメソッドから呼び出された結果として発生します。プログラミング時エラーは、通常、即時かつ決定的なものです。一方、実行時エラーは、データベース接続の枯渇やデータ関連の問題の発生など、任意に発生する何らかの条件に応答してプログラムが実行されるときに発生する障害を表します。実行時エラーは、プログラムがロードやデータの発生に応答してこれらの状態に遭遇するため、実行中のアプリケーションのログに表示される可能性が高くなります。

.. Since runtime errors are not as easy to reproduce and often occur in response to some arbitrary condition as the program runs, they are more difficult to debug and also affect programs that have already been put into production. Within this section, the goal is to try to provide background on some of themost common runtime errors as well as programming time errors.

実行時エラーは再現が容易ではなく、プログラムの実行中に何らかの任意の条件に応じて発生することが多いため、デバッグがより困難になり、また、すでにプロダクション環境に置かれているプログラムにも影響を与えます。このセクションでは、最も一般的な実行時エラーとプログラミング時エラーのバックグラウンドを説明します。

Connections and Transactions
----------------------------

.. _error_3o7r:

QueuePool limit of size <x> overflow <y> reached, connection timed out, timeout <z>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This is possibly the most common runtime error experienced, as it directly involves the work load of the application surpassing a configured limit, one which typically applies to nearly all SQLAlchemy applications.

これは、アプリケーションの作業負荷が設定された制限を超えることに直接関係するため、おそらく最も一般的なランタイムエラーであり、通常、ほとんどすべてのSQLAlchemyアプリケーションに適用されます。

.. The following points summarize what this error means, beginning with the most fundamental points that most SQLAlchemy users should already be familiar with.

以下に、このエラーが何を意味するかをまとめます。まず、ほとんどのSQLAlchemyユーザが既に知っているはずの最も基本的な点から説明します。

.. * **The SQLAlchemy Engine object uses a pool of connections by default** - What this means is that when one makes use of a SQL database connection resourc of an :class:`_engine.Engine` object, and then :term:`releases` that resource, the database connection itself remains connected to the database and is returned to an internal queue where it can be used again.  Even though the code may appear to be ending its conversation with the database, in many cases the application will still maintain a fixed number of database connections that persist until the application ends or the pool is explicitly disposed.

* **SQLAlchemy Engineオブジェクトはデフォルトで接続プールを使用します** - これが意味するのは、 :class:`_engine.Engine` オブジェクトのSQLデータベース接続リソースを使用し、そのリソースを :term:`releases` した場合、データベース接続自体はデータベースに接続されたまま内部キューに戻され、そこで再び使用できるということです。コードがデータベースとの対話を終了しているように見えても、多くの場合、アプリケーションはアプリケーションが終了するか、プールが明示的に破棄されるまで、固定された数のデータベース接続を維持します。

.. * Because of the pool, when an application makes use of a SQL database connection, most typically from either making use of :meth:`_engine.Engine.connect` or when making queries using an ORM :class:`.Session`, this activity does not necessarily establish a new connection to the database at the moment the connection object is acquired; it instead consults the connection pool for a connection, which will often retrieve an existing connection from the pool to be re-used. If no connections are available, the pool will create a new database connection, but only if the pool has not surpassed a configured capacity.

* プールのため、アプリケーションがSQLデータベース接続を使用する場合、最も一般的には :meth:`_engine.Engine.connect` を使用する場合、またはORM :class:`.Session` を使用してクエリを行う場合、このアクティビティは、接続オブジェクトが取得された時点でデータベースへの新しい接続を確立するとは限りません。代わりに、接続プールに接続を問い合わせ、多くの場合、既存の接続をプールから取得して再利用します。使用可能な接続がない場合、プールは新しいデータベース接続を作成しますが、プールが設定された容量を超えていない場合に限られます。

.. * The default pool used in most cases is called :class:`.QueuePool`. When you ask this pool to give you a connection and none are available, it will create a new connection **if the total number of connections in play are less than a configured value**. This value is equal to the **pool size plus the max overflow**. That means if you have configured your engine as::

* ほとんどの場合、デフォルトのプールは :class:`.QueuePool` と呼ばれます。このプールに接続を要求しても使用可能な接続がない場合、新しい接続が作成されます。 **実行中の接続の合計数が設定された値よりも少ない場合** 新しい接続が作成されます。この値は、 **プールサイズに最大オーバーフローを加えた値** に等しくなります。つまり、エンジンを次のように設定した場合::

    engine = create_engine("mysql+mysqldb://u:p@host/db", pool_size=10, max_overflow=20)

..   The above :class:`_engine.Engine` will allow **at most 30 connections** to be in play at any time, not including connections that were detached from the engine or invalidated.  If a request for a new connection arrives and 30 connections are already in use by other parts of the application, the connection pool will block for a fixed period of time, before timing out and raising this error message.

  上記の :class`_engine.Engine` では、エンジンから切り離された接続や無効にされた接続を除き、常に **最大30個の接続** を使用できます。新しい接続の要求が到着し、30個の接続がアプリケーションの他の部分ですでに使用されている場合、接続プールはタイムアウトしてこのエラーメッセージが表示される前に、一定期間ブロックされます。

..   In order to allow for a higher number of connections be in use at once, the pool can be adjusted using the :paramref:`_sa.create_engine.pool_size` and :paramref:`_sa.create_engine.max_overflow` parameters as passed to the :func:`_sa.create_engine` function.      The timeout to wait for a connection to be available is configured using the :paramref:`_sa.create_engine.pool_timeout` parameter.

より多くの接続を一度に使用できるようにするために、 :func:`_sa.create_engine` 関数に渡される :paramref:`_sa.create_engine.pool_size` および: paramref:`_sa.create_engine.max_overflow` パラメータを使用してプールを調整できます。接続が使用可能になるのを待つタイムアウトは、 :paramref:`_sa.create_engine.pool_timeout` パラメータを使用して設定されます。

.. * The pool can be configured to have unlimited overflow by setting :paramref:`_sa.create_engine.max_overflow` to the value "-1".  With this setting, the pool will still maintain a fixed pool of connections, however it will never block upon a new connection being requested; it will instead unconditionally make a new connection if none are available.

* :paramref:`_sa.create_engine.max_overflow` を値"-1"に設定することで、無制限のオーバーフローを持つようにプールを設定できます。この設定では、プールは接続の固定プールを維持しますが、新しい接続が要求されたときにブロックされることはありません。代わりに、使用可能な接続がない場合は無条件に新しい接続を作成します。

..   However, when running in this way, if the application has an issue where it is using up all available connectivity resources, it will eventually hit the configured limit of available connections on the database itself, which will again return an error.  More seriously, when the application exhausts the database of connections, it usually will have caused a great amount of  resources to be used up before failing, and can also interfere with other applications and database status mechanisms that rely upon being able to connect to the database.

  ただし、この方法で実行している場合、使用可能なすべての接続リソースを消費する問題がアプリケーションに発生すると、最終的にはデータベース自体で使用可能な接続の制限に達し、再びエラーが返されます。さらに深刻なことに、アプリケーションがデータベースの接続を消費すると、通常、障害が発生する前に大量のリソースが消費され、データベースへの接続に依存する他のアプリケーションやデータベースのステータス・メカニズムに干渉する可能性もあります。

..   Given the above, the connection pool can be looked at as a **safety valve for connection use**, providing a critical layer of protection against a rogue application causing the entire database to become unavailable to all other applications.   When receiving this error message, it is vastly preferable to repair the issue using up too many connections and/or configure the limits appropriately, rather than allowing for unlimited overflow which does not actually solve the underlying issue.

  上記を考慮すると、接続プールは、データベース全体が他のすべてのアプリケーションから使用できなくなる不正なアプリケーションに対する重要な保護レイヤーを提供する、 **接続使用の安全弁** と見なすことができます。このエラーメッセージを受け取った場合は、根本的な問題を実際に解決しない無制限のオーバーフローを許可するのではなく、過剰な接続を使用して問題を修復したり、制限を適切に設定したりすることが非常に望ましいです。

.. What causes an application to use up all the connections that it has available?

アプリケーションが利用可能なすべての接続を使い切る原因は何ですか?

.. * **The application is fielding too many concurrent requests to do work based on the configured value for the pool** - This is the most straightforward cause.  If you have an application that runs in a thread pool that allows for 30 concurrent threads, with one connection in use per thread, if your pool is not configured to allow at least 30 connections checked out at once, you will get this error once your application receives enough concurrent requests. Solution is to raise the limits on the pool or lower the number of concurrent threads.

* **プールに構成された値に基づいて作業するには、アプリケーションが処理している同時リクエストが多すぎます** - これが最も直接的な原因です。30の同時スレッドを許可するスレッドプールで実行されるアプリケーションがあり、スレッドごとに1つの接続が使用されている場合、プールが一度に少なくとも30の接続をチェックアウトできるように構成されていないと、アプリケーションが十分な同時リクエストを受け取ると、このエラーが発生します。解決策は、プールの制限を上げるか、同時スレッドの数を減らすことです。

.. * **The application is not returning connections to the pool** - This is the next most common reason, which is that the application is making use of the connection pool, but the program is failing to :term:`release` these connections and is instead leaving them open.   The connection pool as well as the ORM :class:`.Session` do have logic such that when the session and/or connection object is garbage collected, it results in the underlying connection resources being released, however this behavior cannot be relied upon to release resources in a timely manner.

* **アプリケーションがプールへの接続を返していないません** - これは次に多い理由で、アプリケーションは接続プールを利用していますが、プログラムがこれらの接続を :term:`release` できず、代わりに開いたままにしています。接続プールとORM :class:`.Session` には、セッションや接続オブジェクトがガベージコレクションされると、基礎となる接続リソースが解放されるようなロジックがありますが、この動作を信頼してリソースをタイムリーに解放することはできません。

..   A common reason this can occur is that the application uses ORM sessions and does not call :meth:`.Session.close` upon them one the work involving that session is complete. Solution is to make sure ORM sessions if using the ORM, or engine-bound :class:`_engine.Connection` objects if using Core, are explicitly closed at the end of the work being done, either via the appropriate ``.close()`` method, or by using one of the available context managers (e.g.  "with:" statement) to properly release the resource.

  これが発生する一般的な理由は、アプリケーションがORMセッションを使用しており、そのセッションを含む作業が完了しても :meth:`.Session.close` を呼び出さないためです。解決策は、ORMを使用している場合はORMセッションを、Coreを使用している場合はエンジンにバインドされた :class:`_engine.Connection` オブジェクトを、適切な ``close()`` メソッドを使用するか、利用可能なコンテキストマネージャ(例えば"with:"文)の1つを使用してリソースを適切に解放することによって、行われている作業の最後に明示的に閉じるようにすることです。

.. * **The application is attempting to run long-running transactions** - A database transaction is a very expensive resource, and should **never be left idle waiting for some event to occur**.  If an application is waiting for a user to push a button, or a result to come off of a long running job queue, or is holding a persistent connection open to a browser, **don't keep a database transaction open for the whole time**.  As the application needs to work with the database and interact with an event, open a short-lived transaction at that point and then close it.

* **アプリケーションは長時間実行トランザクションを実行しようとしています** - データベーストランザクションは非常に高価なリソースであり、 **何らかのイベントが発生するのを待ってアイドル状態にしておくべきではありません** 。アプリケーションが、ユーザーがボタンを押すのを待っている場合、長時間実行ジョブキューから結果が返されるのを待っている場合、またはブラウザへの永続的な接続を開いたままにしている場合は、**データベーストランザクションを開いたままにしておく必要はありません**。アプリケーションはデータベースを操作し、イベントと対話する必要があるため、その時点で短時間実行トランザクションを開いてから閉じます。

.. * **The application is deadlocking** - Also a common cause of this error and more difficult to grasp, if an application is not able to complete its use of a connection either due to an application-side or database-side deadlock, the application can use up all the available connections which then leads to additional requests receiving this error.   Reasons for deadlocks include:

* **アプリケーションがデッドロックしています**-これもこのエラーの一般的な原因ですが、アプリケーション側またはデータベース側のデッドロックのためにアプリケーションが接続の使用を完了できない場合、アプリケーションは使用可能なすべての接続を使い果たし、追加の要求がこのエラーを受け取ることになります。デッドロックの理由は次のとおりです。

..   * Using an implicit async system such as gevent or eventlet without properly monkeypatching all socket libraries and drivers, or which has bugs in not fully covering for all monkeypatched driver methods, or less commonly when the async system is being used against CPU-bound workloads and greenlets making use of database resources are simply waiting too long to attend to them.  Neither implicit nor explicit async programming frameworks are typically necessary or appropriate for the vast majority of relational database operations; if an application must use an async system for some area of functionality, it's best that database-oriented business methods run within traditional threads that pass messages to the async part of the application.

    * すべてのソケットライブラリとドライバに適切にモンキーパッチを適用せずに、geventやeventletなどの暗黙的な非同期システムを使用する、またはすべてのモンキーパッチされたドライバメソッドを完全にカバーしていないバグがある、またはあまり一般的ではありませんが、CPUにバインドされたワークロードに対して非同期システムが使用されていて、データベースリソースを利用するグリーンレットが単にそれらに対応するのに時間がかかりすぎる場合。暗黙的にも明示的にも、非同期プログラミングフレームワークは、通常、リレーショナルデータベース操作の大部分に必要または適切ではありません。アプリケーションが機能の一部に非同期システムを使用する必要がある場合、データベース指向のビジネスメソッドは、アプリケーションの非同期部分にメッセージを渡す従来のスレッド内で実行するのが最善です。

..   * A database side deadlock, e.g. rows are mutually deadlocked

  * データベース側のデッドロック。たとえば、ローが相互にデッドロックされている。

..   * Threading errors, such as mutexes in a mutual deadlock, or calling upon an already locked mutex in the same thread

  * 相互デッドロック状態にあるmutexや、同じスレッド内のすでにロックされているmutexの呼び出しなどのスレッド化エラー

.. Keep in mind an alternative to using pooling is to turn off pooling entirely.  See the section :ref:`pool_switching` for background on this.  However, note that when this error message is occurring, it is **always** due to a bigger problem in the application itself; the pool just helps to reveal the problem sooner.

プーリングを使用する代わりに、プーリングを完全にオフにする方法もあることに注意してください。このバックグラウンドについては :ref:`pool_switching` の節を参照してください。ただし、このエラーメッセージが発生している場合は、 **常に** アプリケーション自体のより大きな問題が原因であることに注意してください。プールは問題をより早く明らかにするのに役立ちます。

.. seealso::

 :ref:`pooling_toplevel`

 :ref:`connections_toplevel`

.. _error_pcls:

Pool class cannot be used with asyncio engine (or vice versa)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The :class:`_pool.QueuePool` pool class uses a ``thread.Lock`` object internally and is not compatible with asyncio.  If using the :func:`_asyncio.create_async_engine` function to create an :class:`.AsyncEngine`, the appropriate queue pool class is :class:`_pool.AsyncAdaptedQueuePool`, which is used automatically and does not need to be specified.

:class:`_pool.QueuePool` プールクラスは内部的には ``thread.Lock`` オブジェクトを使用しており、asyncioとは互換性がありません。 :func:`_asyncio. create_async_engine` 関数を使用して :class:`.AsyncEngine` を作成する場合、適切なキュープールクラスは :class:`_pool.AsyncAdaptedQueuePool` です。これは自動的に使用され、指定する必要はありません。

.. In addition to :class:`_pool.AsyncAdaptedQueuePool`, the :class:`_pool.NullPool` and :class:`_pool.StaticPool` pool classes do not use locks and are also suitable for use with async engines.

:class:`_pool.AsyncAdaptedQueuePool` に加えて、 :class:`_pool.NullPool` と :class:`_pool.StaticPool` プールクラスはロックを使用せず、非同期エンジンでの使用にも適しています。

.. This error is also raised in reverse in the unlikely case that the :class:`_pool.AsyncAdaptedQueuePool` pool class is indicated explicitly with the :func:`_sa.create_engine` function.

:class:`_pool.AsyncAdaptedQueuePool` プールクラスが :func:`_sa.create_engine` 関数で明示的に指定されている場合にも、このエラーは逆に発生します。

.. seealso::

    :ref:`pooling_toplevel`

.. _error_8s2b:

Can't reconnect until invalid transaction is rolled back.  Please rollback() fully before proceeding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This error condition refers to the case where a :class:`_engine.Connection` was invalidated, either due to a database disconnect detection or due to an explicit call to :meth:`_engine.Connection.invalidate`, but there is still a transaction present that was initiated either explicitly by the :meth:`_engine.Connection.begin` method, or due to the connection automatically beginning a transaction as occurs in the 2.x series of SQLAlchemy when any SQL statements are emitted.  When a connection is invalidated, any :class:`_engine.Transaction` that was in progress is now in an invalid state, and must be explicitly rolled back in order to remove it from the :class:`_engine.Connection`.

このエラー条件は、データベースの切断が検出されたか、 :meth:`_engine.Connection.invalidate` が明示的に呼び出されたために :class:`_engine.Connection` が無効になったが、 :meth:`_engine.Connection.begin` メソッドによって明示的に開始されたトランザクションがまだ存在する場合、またはSQL文が発行されたときにSQLAlchemyの2.xシリーズで発生するように接続が自動的にトランザクションを開始した場合に発生します。接続が無効になると、進行中だった :class:`_engine.Transaction` は無効な状態になり、 :class:`_engine.Connection` から削除するために明示的にロールバックする必要があります。

.. _error_dbapi:

DBAPI Errors
------------

.. The Python database API, or DBAPI, is a specification for database drivers which can be located at `Pep-249 <https://www.python.org/dev/peps/pep-0249/>`_.  This API specifies a set of exception classes that accommodate the full range of failure modes of the database.

PythonデータベースAPI(DBAPI)は、 `Pep-249 <https://www.python.org/dev/peps/pep-0249/>`_ にあるデータベースドライバの仕様です。このAPIは、データベースのあらゆる障害モードに対応する一連の例外クラスを指定します。

.. SQLAlchemy does not generate these exceptions directly.  Instead, they are intercepted from the database driver and wrapped by the SQLAlchemy-provided exception :class:`.DBAPIError`, however the messaging within the exception is **generated by the driver, not SQLAlchemy**.

SQLAlchemyはこれらの例外を直接生成しません。代わりに、それらはデータベースドライバからインターセプトされ、SQLAlchemyが提供する例外 :class:`.DBAPIError` によってラップされますが、例外内のメッセージは **SQLAlchemyではなく、ドライバによって生成されます** 。

.. _error_rvf5:

InterfaceError
~~~~~~~~~~~~~~

.. Exception raised for errors that are related to the database interface rather than the database itself.

データベース自体ではなく、データベースインターフェースに関連するエラーに対して発生する例外です。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

.. The ``InterfaceError`` is sometimes raised by drivers in the context of the database connection being dropped, or not being able to connect to the database.   For tips on how to deal with this, see the section :ref:`pool_disconnects`.

``InterfaceError`` は、データベース接続が切断されたり、データベースに接続できない状況で、ドライバによって発生することがあります。この問題に対処するためのヒントについては、 :ref:`pool_disconnects` を参照してください。

.. _error_4xp6:

DatabaseError
~~~~~~~~~~~~~

.. Exception raised for errors that are related to the database itself, and not the interface or data being passed.

渡されるインタフェースまたはデータではなく、データベース自体に関連するエラーに対して発生する例外です。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

.. _error_9h9h:

DataError
~~~~~~~~~

.. Exception raised for errors that are due to problems with the processed data like division by zero, numeric value out of range, etc.

ゼロによる除算、範囲外の数値など、処理されたデータの問題に起因するエラーに対して発生する例外です。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

.. _error_e3q8:

OperationalError
~~~~~~~~~~~~~~~~

.. Exception raised for errors that are related to the database's operation and not necessarily under the control of the programmer, e.g. an unexpected disconnect occurs, the data source name is not found, a transaction could not be processed, a memory allocation error occurred during processing, etc.

データベースの操作に関連し、必ずしもプログラマの制御下にないエラーに対して発生する例外です。たとえば、予期しない切断が発生した、データソース名が見つからなかった、トランザクションを処理できなかった、処理中にメモリ割り当てエラーが発生したなど。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

.. The ``OperationalError`` is the most common (but not the only) error class used by drivers in the context of the database connection being dropped, or not being able to connect to the database.   For tips on how to deal with this, see the section :ref:`pool_disconnects`.

``OperationalError`` は最も一般的な(しかし唯一ではない)エラークラスで、データベース接続が切断されたり、データベースに接続できなくなったりした場合にドライバが使用します。これに対処するためのヒントについては :ref:`pool_disconnects` を参照してください。

.. _error_gkpj:

IntegrityError
~~~~~~~~~~~~~~

.. Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.

外部キーチェックが失敗するなど、データベースのリレーショナル整合性が影響を受ける場合に発生する例外です。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

.. _error_2j85:

InternalError
~~~~~~~~~~~~~

.. Exception raised when the database encounters an internal error, e.g. the cursor is not valid anymore, the transaction is out of sync, etc.

データベースで内部エラーが発生した場合に発生する例外です。たとえば、カーソルが無効になった、トランザクションが同期していないなどです。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

.. The ``InternalError`` is sometimes raised by drivers in the context of the database connection being dropped, or not being able to connect to the database.   For tips on how to deal with this, see the section :ref:`pool_disconnects`.

``InternalError`` は、データベース接続が切断されたり、データベースに接続できなかったりする状況で、ドライバによって発生することがあります。この問題に対処するためのヒントについては、 :ref:`pool_disconnects` を参照してください。

.. _error_f405:

ProgrammingError
~~~~~~~~~~~~~~~~

.. Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.

プログラミングエラーの場合に発生する例外です。たとえば、テーブルが見つからない、またはすでに存在する、SQL文の構文エラー、指定されたパラメータの数が間違っているなど。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

.. The ``ProgrammingError`` is sometimes raised by drivers in the context of the database connection being dropped, or not being able to connect to the database.   For tips on how to deal with this, see the section :ref:`pool_disconnects`.

データベース接続が切断された場合や、データベースに接続できない場合に、ドライバによって ``ProgrammingError`` が発生することがあります。これに対処するためのヒントについては、 :ref:`pool_disconnects` を参照してください。

.. _error_tw8g:

NotSupportedError
~~~~~~~~~~~~~~~~~

.. Exception raised in case a method or database API was used which is not supported by the database, e.g. requesting a .rollback() on a connection that does not support transaction or has transactions turned off.

データベースでサポートされていないメソッドまたはデータベースAPIが使用された場合に発生する例外です。たとえば、トランザクションをサポートしていない接続またはトランザクションがオフになっている接続で .rollback()を要求した場合などです。

.. This error is a :ref:`DBAPI Error <error_dbapi>` and originates from the database driver (DBAPI), not SQLAlchemy itself.

このエラーは :ref:`DBAPI Error <error_dbapi>` であり、SQLAlchemy自身ではなく、データベースドライバ(DBAPI)から発生します。

SQL Expression Language
-----------------------
.. _error_cprf:
.. _caching_caveats:

Object will not produce a cache key, Performance Implications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. SQLAlchemy as of version 1.4 includes a :ref:`SQL compilation caching facility <sql_caching>` which will allow Core and ORM SQL constructs to cache their stringified form, along with other structural information used to fetch results from the statement, allowing the relatively expensive string compilation process to be skipped when another structurally equivalent construct is next used. This system relies upon functionality that is implemented for all SQL constructs, including objects such as  :class:`_schema.Column`, :func:`_sql.select`, and :class:`_types.TypeEngine` objects, to produce a **cache key** which fully represents their state to the degree that it affects the SQL compilation process.

バージョン1.4のSQLAlchemyには :ref:`SQL compilation caching facility <sql_caching>` が含まれています。これにより、CoreとORM SQL構文が、結果を文から取得するために使用される他の構造情報と共に、文字列化された形式をキャッシュできるようになり、構造的に等価な別の構文が次に使用されるときに、比較的高価な文字列コンパイルプロセスをスキップできるようになります。このシステムは、 :class:`_schema.Column` 、 :func:`_sql.select` 、 :class:`_types.TypeEngine` オブジェクトなどのオブジェクトを含むすべてのSQL構文に実装されている機能に依存して、SQLコンパイルプロセスに影響を与える程度までそれらの状態を完全に表現する **キャッシュキー** を生成します。

.. If the warnings in question refer to widely used objects such as :class:`_schema.Column` objects, and are shown to be affecting the majority of SQL constructs being emitted (using the estimation techniques described at :ref:`sql_caching_logging`) such that caching is generally not enabled for an application, this will negatively impact performance and can in some cases effectively produce a **performance degradation** compared to prior SQLAlchemy versions. The FAQ at :ref:`faq_new_caching` covers this in additional detail.

問題の警告が :class:`_schema.Column` オブジェクトのような広く使用されているオブジェクトを参照していて、( :ref:`sql_caching_logging` で説明されている推定テクニックを使って)発行されるSQL構文の大部分に影響を与えていることが示され、一般的にアプリケーションでキャッシングが有効になっていない場合、これはパフォーマンスに悪影響を与え、場合によっては以前のバージョンのSQLAlchemyと比較して **パフォーマンスの低下** を引き起こす可能性があります。 :ref:`faq_new_caching` のFAQでは、これについてさらに詳しく説明しています。



Caching disables itself if there's any doubt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Caching relies on being able to generate a cache key that accurately represents the **complete structure** of a statement in a **consistent** fashion. If a particular SQL construct (or type) does not have the appropriate directives in place which allow it to generate a proper cache key, then caching cannot be safely enabled:

キャッシュは、文の **完全な構造** を **一貫性のある** 方法で正確に表すキャッシュキーを生成できるかどうかに依存します。特定のSQL構文(または型)に、適切なキャッシュキーの生成を可能にする適切なディレクティブがない場合、キャッシュを安全に有効化できません。

.. * The cache key must represent the **complete structure**: If the usage of two separate instances of that construct may result in different SQL being rendered, caching the SQL against the first instance of the element using a cache key that does not capture the distinct differences between the first and second elements will result in incorrect SQL being cached and rendered for the second instance.

* キャッシュキーは **完全な構造** を表している必要があります。その構文の2つの別々のインスタンスを使用すると異なるSQLがレンダリングされる可能性がある場合、最初の要素と2番目の要素の明確な違いを取得しないキャッシュキーを使用して、要素の最初のインスタンスに対してSQLをキャッシュすると、2番目のインスタンスに対して不正なSQLがキャッシュされてレンダリングされます。

.. * The cache key must be **consistent**: If a construct represents state that changes every time, such as a literal value, producing unique SQL for every instance of it, this construct is also not safe to cache, as repeated use of the construct will quickly fill up the statement cache with unique SQL strings that will likely not be used again, defeating the purpose of the cache.

* キャッシュキーは **一貫性がある** 必要があります。構文が毎回変化する状態(リテラル値など)を表し、そのすべてのインスタンスに対して一意のSQLを生成する場合、この構文をキャッシュしても安全ではありません。これは、構文を繰り返し使用すると、文キャッシュが一意のSQL文字列ですぐにいっぱいになり、二度と使用されない可能性が高いため、キャッシュの目的が損なわれるためです。

.. For the above two reasons, SQLAlchemy's caching system is **extremely conservative** about deciding to cache the SQL corresponding to an object.

上記の2つの理由から、SQLAlchemyのキャッシュシステムは、オブジェクトに対応するSQLをキャッシュすることを決定することに関して **非常に保守的** です。

Assertion attributes for caching
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. The warning is emitted based on the criteria below.  For further detail on each, see the section :ref:`faq_new_caching`.

この警告は以下の基準に基づいて発せられます。それぞれの詳細については :ref:`faq_new_caching` を参照してください。

.. * The :class:`.Dialect` itself (i.e. the module that is specified by the first part of the URL we pass to :func:`_sa.create_engine`, like ``postgresql+psycopg2://``), must indicate it has been reviewed and tested to support caching correctly, which is indicated by the :attr:`.Dialect.supports_statement_cache` attribute being set to ``True``.  When using third party dialects, consult with the maintainers of the dialect so that they may follow the :ref:`steps to ensure caching may be enabled <engine_thirdparty_caching>` in their dialect and publish a new release.

* :class:`.Dialect` 自体(つまり、 :func:`_sa.create_engine` に渡すURLの最初の部分で指定されるモジュール。例えば、 ``postgresql+psycopg2://`` )は、キャッシュを正しくサポートするためにレビューされ、テストされたことを示す必要があります。これは、 :attr:`.Dialect.supports_statement_cache` 属性が ``True`` に設定されていることで示されます。サードパーティのダイアレクトを使用する場合は、ダイアレクトのメンテナに相談して、彼らのダイアレクトで :ref:`steps to ensure caching may be enabled <engine_thirdparty_caching>` に従って新しいリリースを公開してください。

.. * Third party or user defined types that inherit from either :class:`.TypeDecorator` or :class:`.UserDefinedType` must include the :attr:`.ExternalType.cache_ok` attribute in their definition, including for all derived subclasses, following the guidelines described in the docstring for :attr:`.ExternalType.cache_ok`. As before, if these datatypes are imported from third party libraries, consult with the maintainers of that library so that they may provide the necessary changes to their library and publish a new release.

* :class:`.TypeDecorator` または :class:`.UserDefinedType` のいずれかを継承するサードパーティまたはユーザ定義の型は、 :attr:`.ExternalType.cache_ok` 属性をその定義に含める必要があります。これには 、:attr:`.ExternalType.cache_ok` のdocstringで説明されているガイドラインに従って、すべての派生サブクラスも含まれます。以前と同様に、これらのデータ型がサードパーティのライブラリからインポートされている場合は、そのライブラリのメンテナと相談して、ライブラリに必要な変更を加え、新しいリリースを公開してください。

.. * Third party or user defined SQL constructs that subclass from classes such as :class:`.ClauseElement`, :class:`_schema.Column`, :class:`_dml.Insert` etc, including simple subclasses as well as those which are designed to work with the :ref:`sqlalchemy.ext.compiler_toplevel`, should normally include the :attr:`.HasCacheKey.inherit_cache` attribute set to ``True`` or ``False`` based on the design of the construct, following the guidelines described at :ref:`compilerext_caching`.

* :class:`.ClauseElement` 、 :class:`_schema.Column` 、 :class:`_dml.Insert` などのクラスをサブクラスとするサードパーティまたはユーザ定義のSQL構文は、単純なサブクラスや :ref:`sqlalchemy.ext.compiler_toplevel` で動作するように設計されたサブクラスも含めて、通常は :ref:`compilerext_caching` で説明されているガイドラインに従って、構文の設計に基づいて :attr:`.HasCacheKey.inherit_cache` 属性を ``True`` または ``False`` に設定する必要があります。

.. seealso::

    .. :ref:`sql_caching_logging` - background on observing cache behavior and efficiency

    :ref:`sql_caching_logging` - キャッシュの動作と効率を観測したバックグラウンド

    .. :ref:`faq_new_caching` - in the :ref:`faq_toplevel` section

    :ref:`faq_new_caching` - :ref:`faq_toplevel` セクション

.. _error_l7de:

Compiler StrSQLCompiler can't render element of type <element type>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This error usually occurs when attempting to stringify a SQL expression construct that includes elements which are not part of the default compilation; in this case, the error will be against the :class:`.StrSQLCompiler` class.  In less common cases, it can also occur when the wrong kind of SQL expression is used with a particular type of database backend; in those cases, other kinds of SQL compiler classes will be named, such as ``SQLCompiler`` or ``sqlalchemy.dialects.postgresql.PGCompiler``.  The guidance below is more specific to the "stringification" use case but describes the general background as well.

このエラーは通常、デフォルトのコンパイルの一部ではない要素を含むSQL式の構成体を文字列化しようとしたときに発生します。この場合、エラーは :class:`.StrSQLCompiler` クラスに対して発生します。あまり一般的ではありませんが、特定の種類のデータベースバックエンドで間違った種類のSQL式が使用された場合にも発生することがあります。そのような場合には、 ``SQLCompiler`` や ``sqlalchemy.dialects.postgresql.PGCompiler`` など、他の種類のSQLコンパイラクラスに名前が付けられます。以下のガイダンスは、"文字列化"のユースケースに特化していますが、一般的なバックグラウンドについても説明しています。

.. Normally, a Core SQL construct or ORM :class:`_query.Query` object can be stringified directly, such as when we use ``print()``:

通常、コアSQL構文またはORM :class:`_query.Query` オブジェクトは、 ``print()`` のように直接文字列化することができます。

.. sourcecode:: pycon+sql

  >>> from sqlalchemy import column
  >>> print(column("x") == 5)
  {printsql}x = :x_1

.. When the above SQL expression is stringified, the :class:`.StrSQLCompiler` compiler class is used, which is a special statement compiler that is invoked when a construct is stringified without any dialect-specific information.

上記のSQL式が文字列化されると、 :class:`.StrSQLCompiler` コンパイラクラスが使用されます。これは、構文が方言固有の情報なしに文字列化されたときに呼び出される特別なステートメントコンパイラです。

.. However, there are many constructs that are specific to some particular kind of database dialect, for which the :class:`.StrSQLCompiler` doesn't know how to turn into a string, such as the PostgreSQL `"insert on conflict" <postgresql_insert_on_conflict>`_ construct::

しかし、ある特定の種類のデータベース言語に固有の多くの構文があります。例えば、PostgreSQLの `"insert on conflict" <PostgreSQL_insert_on_conflict>`_ 構文のように、  :class:`.StrSQLCompiler` は文字列に変換する方法を知りません::

  >>> from sqlalchemy.dialects.postgresql import insert
  >>> from sqlalchemy import table, column
  >>> my_table = table("my_table", column("x"), column("y"))
  >>> insert_stmt = insert(my_table).values(x="foo")
  >>> insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["y"])
  >>> print(insert_stmt)
  Traceback (most recent call last):

  ...

  sqlalchemy.exc.UnsupportedCompilationError: Compiler <sqlalchemy.sql.compiler.StrSQLCompiler object at 0x7f04fc17e320> can't render element of type <class 'sqlalchemy.dialects.postgresql.dml.OnConflictDoNothing'>

.. In order to stringify constructs that are specific to particular backend, the :meth:`_expression.ClauseElement.compile` method must be used, passing either an :class:`_engine.Engine` or a :class:`.Dialect` object which will invoke the correct compiler.   Below we use a PostgreSQL dialect:

特定のバックエンドに固有の構文を文字列化するには、 :meth:`_expression.ClauseElement.compile` メソッドを使用して、正しいコンパイラを呼び出す :class:`_engine.Engine` または :class:`.Dialect` オブジェクトを渡す必要があります。以下ではPostgreSQLのダイアレクトを使用します:

.. sourcecode:: pycon+sql

  >>> from sqlalchemy.dialects import postgresql
  >>> print(insert_stmt.compile(dialect=postgresql.dialect()))
  {printsql}INSERT INTO my_table (x) VALUES (%(x)s) ON CONFLICT (y) DO NOTHING

.. For an ORM :class:`_query.Query` object, the statement can be accessed using the :attr:`~.orm.query.Query.statement` accessor::

ORM :class:`_query.Query` オブジェクトの場合、この文は :attr:`~.orm.query.Query.statement` アクセッサを使ってアクセスできます::

    statement = query.statement
    print(statement.compile(dialect=postgresql.dialect()))

.. See the FAQ link below for additional detail on direct stringification / compilation of SQL elements.

SQL要素の直接のストリング化/コンパイルの詳細については、以下のFAQリンクを参照してください。

.. seealso::

  :ref:`faq_sql_expression_string`


TypeError: <operator> not supported between instances of 'ColumnProperty' and <something>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This often occurs when attempting to use a :func:`.column_property` or :func:`.deferred` object in the context of a SQL expression, usually within declarative such as::

これは、 :func:`.column_property` または :func:`.deferred` オブジェクトをSQL式のコンテキストで、通常は次のような宣言内で使用しようとしたときによく起こります::

    class Bar(Base):
        __tablename__ = "bar"

        id = Column(Integer, primary_key=True)
        cprop = deferred(Column(Integer))

        __table_args__ = (CheckConstraint(cprop > 5),)

.. Above, the ``cprop`` attribute is used inline before it has been mapped, however this ``cprop`` attribute is not a :class:`_schema.Column`, it's a :class:`.ColumnProperty`, which is an interim object and therefore does not have the full functionality of either the :class:`_schema.Column` object or the :class:`.InstrumentedAttribute` object that will be mapped onto the ``Bar`` class once the declarative process is complete.

上記では、 ``cprop`` 属性はマップされる前にインラインで使用されていますが、この ``cprop`` 属性は :class:`_schema.Column` ではなく、 :class:`.ColumnProperty` です。これは一時的なオブジェクトなので、宣言プロセスが完了すると ``Bar`` クラスにマップされる :class:`_schema.Column` オブジェクトや :class:`.InstrumentedAttribute` オブジェクトの完全な機能を持ちません。

.. While the :class:`.ColumnProperty` does have a ``__clause_element__()`` method, which allows it to work in some column-oriented contexts, it can't work in an open-ended comparison context as illustrated above, since it has no Python ``__eq__()`` method that would allow it to interpret the comparison to the number "5" as a SQL expression and not a regular Python comparison.

:class:`.ColumnProperty` には、いくつかの列指向のコンテキストで動作することを可能にする ``__clause_element__()`` メソッドがありますが、上で説明したようなオープンエンドの比較コンテキストでは動作しません。なぜなら、数値"5"との比較を通常のPythonの比較ではなくSQL式として解釈できるPythonの ``__eq__()`` メソッドがないからです。

.. The solution is to access the :class:`_schema.Column` directly using the :attr:`.ColumnProperty.expression` attribute::

解決策は、 :attr:`.ColumnProperty.expression` 属性を使って直接 :class:`_schema.Column` にアクセスすることです::

    class Bar(Base):
        __tablename__ = "bar"

        id = Column(Integer, primary_key=True)
        cprop = deferred(Column(Integer))

        __table_args__ = (CheckConstraint(cprop.expression > 5),)

.. _error_cd3x:

A value is required for bind parameter <x> (in parameter group <y>)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. THIS ERROR OCCURS WHEN A STATEMENT MAKES USE OF :FUNC:`.BINDPARAM` EITHER IMPLICITLY OR EXPLICITLY AND DOES NOT PROVIDE A VALUE WHEN THE STATEMENT IS EXECUTED::

このエラーは、ステートメントが暗黙的または明示的に :func:`.bindparam` を使用し、ステートメントの実行時に値を提供しない場合に発生します::

    stmt = select(table.c.column).where(table.c.id == bindparam("my_param"))

    result = conn.execute(stmt)

.. Above, no value has been provided for the parameter "my_param".  The correct approach is to provide a value::

上記では、パラメータ"my_param"に値が指定されていません。正しい方法は、値を指定することです::

    result = conn.execute(stmt, {"my_param": 12})

.. When the message takes the form "a value is required for bind parameter <x> in parameter group <y>", the message is referring to the "executemany" style of execution.  In this case, the statement is typically an INSERT, UPDATE, or DELETE and a list of parameters is being passed.   In this format, the statement may be generated dynamically to include parameter positions for every parameter given in the argument list, where it will use the **first set of parameters** to determine what these should be.

メッセージが "a value is required for bind parameter <x> in parameter group <y>"の形式をとる場合、メッセージは"executemany"スタイルの実行を参照しています。この場合、ステートメントは通常INSERT、UPDATE、またはDELETEで、パラメータのリストが渡されます。この形式では、ステートメントは引数リストで指定されたすべてのパラメータのパラメータ位置を含むように動的に生成され、 **最初のパラメータセット** を使用して、これらが何であるべきかを決定します。

.. For example, the statement below is calculated based on the first parameter set to require the parameters, "a", "b", and "c" - these names determine the final string format of the statement which will be used for each set of parameters in the list.  As the second entry does not contain "b", this error is generated::

たとえば、次の文は、パラメータ"a"、"b"、および"c"を必要とする最初のパラメータセットに基づいて計算されます。これらの名前は、リスト内の各パラメータセットに使用される文の最終的な文字列形式を決定します。2番目のエントリに"b"が含まれていないため、このエラーが生成されます::

    m = MetaData()
    t = Table("t", m, Column("a", Integer), Column("b", Integer), Column("c", Integer))

    e.execute(
        t.insert(),
        [
            {"a": 1, "b": 2, "c": 3},
            {"a": 2, "c": 4},
            {"a": 3, "b": 4, "c": 5},
        ],
    )

.. code-block::

 sqlalchemy.exc.StatementError: (sqlalchemy.exc.InvalidRequestError) A value is required for bind parameter 'b', in parameter group 1 [SQL: u'INSERT INTO t (a, b, c) VALUES (?, ?, ?)'] [parameters: [{'a': 1, 'c': 3, 'b': 2}, {'a': 2, 'c': 4}, {'a': 3, 'c': 5, 'b': 4}]]

.. Since "b" is required, pass it as ``None`` so that the INSERT may proceed::

"b"は必須なので、INSERTが実行されるように、"None"として渡します::

    e.execute(
        t.insert(),
        [
            {"a": 1, "b": 2, "c": 3},
            {"a": 2, "b": None, "c": 4},
            {"a": 3, "b": 4, "c": 5},
        ],
    )

.. seealso::

  :ref:`tutorial_sending_parameters`

.. _error_89ve:

Expected FROM clause, got Select.  To create a FROM clause, use the .subquery() method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This refers to a change made as of SQLAlchemy 1.4 where a SELECT statement as generated by a function such as :func:`_expression.select`, but also including things like unions and textual SELECT expressions are no longer considered to be :class:`_expression.FromClause` objects and can't be placed directly in the FROM clause of another SELECT statement without them being wrapped in a :class:`.Subquery` first.   This is a major conceptual change in the Core and the full rationale is discussed at :ref:`change_4617`.

これはSQLAlchemy 1.4で行われた変更で、 :func:`_expression.select` のような関数によって生成され、共用体やテキストのSELECT式のようなものを含むSELECT文は、 :class:`_expression.FromClause` オブジェクトとは見なされなくなり、最初に :class:`.Subquery` でラップされない限り、別のSELECT文のFROM句に直接配置することはできなくなりました。これはコアの主要な概念上の変更であり、完全な理論的根拠は :ref:`change_4617` で議論されています。

Given an example as::

    m = MetaData()
    t = Table("t", m, Column("a", Integer), Column("b", Integer), Column("c", Integer))
    stmt = select(t)

.. Above, ``stmt`` represents a SELECT statement.  The error is produced when we want to use ``stmt`` directly as a FROM clause in another SELECT, such as if we attempted to select from it::

上の例では、 ``stmt`` はSELECT文を表しています。このエラーは、別のSELECTのFROM句として ``stmt`` を直接使用したい場合に発生します。たとえば、そこから選択しようとした場合などです::

    new_stmt_1 = select(stmt)

.. Or if we wanted to use it in a FROM clause such as in a JOIN::

または、JOINなどのFROM句で使用する場合::

    new_stmt_2 = select(some_table).select_from(some_table.join(stmt))

.. In previous versions of SQLAlchemy, using a SELECT inside of another SELECT would produce a parenthesized, unnamed subquery.   In most cases, this form of SQL is not very useful as databases like MySQL and PostgreSQL require that subqueries in FROM clauses have named aliases, which means using the :meth:`_expression.SelectBase.alias` method or as of 1.4 using the :meth:`_expression.SelectBase.subquery` method to produce this.   On other databases, it is still much clearer for the subquery to have a name to resolve any ambiguity on future references to column  names inside the subquery.

以前のバージョンのSQLAlchemyでは、別のSELECTの内部でSELECTを使用すると、括弧で括られた名前のない副問い合わせが生成されました。MySQLやPostgreSQLのようなデータベースでは、FROM句内の副問い合わせが名前付きのエイリアスを持つ必要があるため、ほとんどの場合、この形式のSQLはあまり有用ではありません。つまり、 :meth:`_expression.SelectBase.alias` メソッドを使用するか、1.4では :meth:`_expression.SelectBase.subquery` メソッドを使用してこれを生成します。他のデータベースでは、副問い合わせ内の列名への将来の参照に関するあいまいさを解決するために、副問い合わせが名前を持つ方がはるかに明確です。

.. Beyond the above practical reasons, there are a lot of other SQLAlchemy-oriented reasons the change is being made.  The correct form of the above two statements therefore requires that :meth:`_expression.SelectBase.subquery` is used::

上記の実際的な理由以外にも、変更が行われているSQLAlchemy指向の理由はたくさんあります。したがって、上記の2つのステートメントの正しい形式では、 :meth:`_expression.SelectBase.subquery` を使用する必要があります::

    subq = stmt.subquery()

    new_stmt_1 = select(subq)

    new_stmt_2 = select(some_table).select_from(some_table.join(subq))

.. seealso::

  :ref:`change_4617`

.. _error_xaj1:

An alias is being generated automatically for raw clauseelement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.4.26

.. This deprecation warning refers to a very old and likely not well known pattern that applies to the legacy :meth:`_orm.Query.join` method as well as the :term:`2.0 style` :meth:`_sql.Select.join` method, where a join can be stated in terms of a :func:`_orm.relationship` but the target is the :class:`_schema.Table` or other Core selectable to which the class is mapped, rather than an ORM entity such as a mapped class or :func:`_orm.aliased` construct::

この非推奨警告は、レガシーの :meth:`_orm.Query.join` メソッドと :term:`2.0 style` :meth:`_sql.Select.join` メソッドに適用される非常に古く、あまり知られていないパターンを参照しています。ここで、結合は :func:`_orm.relationship` で記述できますが、ターゲットは、マップされたクラスや :func:`_orm.aliased` 構成体のようなORMエンティティではなく、クラスがマップされる :class:`_schema.Table` やその他のCore選択可能なものです::

    a1 = Address.__table__

    q = (
        s.query(User)
        .join(a1, User.addresses)
        .filter(Address.email_address == "ed@foo.com")
        .all()
    )

.. The above pattern also allows an arbitrary selectable, such as a Core :class:`_sql.Join` or :class:`_sql.Alias` object, however there is no automatic adaptation of this element, meaning the Core element would need to be referenced directly::

上記のパターンでは、Core :class:`_sql.Join` や :class:`_sql.Alias` オブジェクトのような任意の選択が可能ですが、この要素は自動的には適用されないので、Core要素を直接参照する必要があります::

    a1 = Address.__table__.alias()

    q = (
        s.query(User)
        .join(a1, User.addresses)
        .filter(a1.c.email_address == "ed@foo.com")
        .all()
    )

.. The correct way to specify a join target is always by using the mapped class itself or an :class:`_orm.aliased` object, in the latter case using the :meth:`_orm.PropComparator.of_type` modifier to set up an alias::

結合対象を指定する正しい方法は、常にマップされたクラスそのものか :class:`_orm.aliased` オブジェクトを使うことです。後者の場合は :meth:`_orm.PropComparator.of_type` 修飾子を使ってエイリアスを設定します::

    # normal join to relationship entity
    q = s.query(User).join(User.addresses).filter(Address.email_address == "ed@foo.com")

    # name Address target explicitly, not necessary but legal
    q = (
        s.query(User)
        .join(Address, User.addresses)
        .filter(Address.email_address == "ed@foo.com")
    )

.. Join to an alias::

エイリアスへの結合::

    from sqlalchemy.orm import aliased

    a1 = aliased(Address)

    # of_type() form; recommended
    q = (
        s.query(User)
        .join(User.addresses.of_type(a1))
        .filter(a1.email_address == "ed@foo.com")
    )

    # target, onclause form
    q = s.query(User).join(a1, User.addresses).filter(a1.email_address == "ed@foo.com")

.. _error_xaj2:

An alias is being generated automatically due to overlapping tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.4.26

.. This warning is typically generated when querying using the :meth:`_sql.Select.join` method or the legacy :meth:`_orm.Query.join` method with mappings that involve joined table inheritance. The issue is that when joining between two joined inheritance models that share a common base table, a proper SQL JOIN between the two entities cannot be formed without applying an alias to one side or the other; SQLAlchemy applies an alias to the right side of the join. For example given a joined inheritance mapping as::

この警告は通常、 :meth:`_sql.Select.join` メソッドまたは従来の :meth:`_orm.Query.join` メソッドを使用して、結合テーブルの継承を含むマッピングでクエリを行うときに生成されます。問題は、共通のベーステーブルを共有する2つの結合された継承モデル間を結合する場合、2つのエンティティ間の適切なSQL JOINは、どちらかの側にエイリアスを適用しないと形成できないことです。SQLAlchemyは、結合の右側にエイリアスを適用します。たとえば、結合された継承マッピングが次のように与えられたとします::

    class Employee(Base):
        __tablename__ = "employee"
        id = Column(Integer, primary_key=True)
        manager_id = Column(ForeignKey("manager.id"))
        name = Column(String(50))
        type = Column(String(50))

        reports_to = relationship("Manager", foreign_keys=manager_id)

        __mapper_args__ = {
            "polymorphic_identity": "employee",
            "polymorphic_on": type,
        }


    class Manager(Employee):
        __tablename__ = "manager"
        id = Column(Integer, ForeignKey("employee.id"), primary_key=True)

        __mapper_args__ = {
            "polymorphic_identity": "manager",
            "inherit_condition": id == Employee.id,
        }

.. The above mapping includes a relationship between the ``Employee`` and ``Manager`` classes.  Since both classes make use of the "employee" database table, from a SQL perspective this is a :ref:`self referential relationship <self_referential>`.  If we wanted to query from both the ``Employee`` and ``Manager`` models using a join, at the SQL level the "employee" table needs to be included twice in the query, which means it must be aliased.   When we create such a join using the SQLAlchemy ORM, we get SQL that looks like the following:

上記のマッピングには、 ``Employee`` クラスと ``Manager`` クラスの間の関係が含まれています。どちらのクラスも ``employee`` データベーステーブルを使用しているので、SQLの観点から見ると、これは :ref:`self_referential relationship <self_referential>` です。結合を使用して ``Employee`` モデルと ``Manager`` モデルの両方からクエリを実行したい場合、SQLレベルでは``employee`` テーブルをクエリに2回含める必要があります。つまり、エイリアスを作成する必要があります。SQLAlchemy ORMを使用してこのような結合を作成すると、次のようなSQLが得られます。

.. sourcecode:: pycon+sql

    >>> stmt = select(Employee, Manager).join(Employee.reports_to)
    >>> print(stmt)
    {printsql}SELECT employee.id, employee.manager_id, employee.name,
    employee.type, manager_1.id AS id_1, employee_1.id AS id_2,
    employee_1.manager_id AS manager_id_1, employee_1.name AS name_1,
    employee_1.type AS type_1
    FROM employee JOIN
    (employee AS employee_1 JOIN manager AS manager_1 ON manager_1.id = employee_1.id)
    ON manager_1.id = employee.manager_id

.. Above, the SQL selects FROM the ``employee`` table, representing the ``Employee`` entity in the query. It then joins to a right-nested join of ``employee AS employee_1 JOIN manager AS manager_1``, where the ``employee`` table is stated again, except as an anonymous alias ``employee_1``. This is the 'automatic generation of an alias' to which the warning message refers.

上の例では、SQLはクエリ内の ``Employee`` エンティティを表す ``employee`` テーブルから選択します。次に、 ``employee AS employee_1 JOIN manager AS manager_1`` の右入れ子結合に結合します。ここでは、匿名のエイリアス ``employee_1`` を除いて、 ``employee`` テーブルが再度記述されています。これは、警告メッセージが参照する"エイリアスの自動生成"です。

.. When SQLAlchemy loads ORM rows that each contain an ``Employee`` and a ``Manager`` object, the ORM must adapt rows from what above is the ``employee_1`` and ``manager_1`` table aliases into those of the un-aliased ``Manager`` class. This process is internally complex and does not accommodate for all API features, notably when trying to use eager loading features such as :func:`_orm.contains_eager` with more deeply nested queries than are shown here.  As the pattern is unreliable for more complex scenarios and involves implicit decisionmaking that is difficult to anticipate and follow, the warning is emitted and this pattern may be considered a legacy feature. The better way to write this query is to use the same patterns that apply to any other self-referential relationship, which is to use the :func:`_orm.aliased` construct explicitly.  For joined-inheritance and other join-oriented mappings, it is usually desirable to add the use of the :paramref:`_orm.aliased.flat` parameter, which will allow a JOIN of two or more tables to be aliased by applying an alias to the individual tables within the join, rather than embedding the join into a new subquery:

SQLAlchemyがそれぞれ ``Employee`` オブジェクトと ``Manager`` オブジェクトを含むORM行をロードする時、ORMは上にある ``employee_1`` と ``manager_1`` というテーブルエイリアスからの行を、エイリアスされていない ``Manager`` クラスの行に適合させなければなりません。このプロセスは内部的に複雑で、すべてのAPI機能に対応しているわけではありません。特に、 :func:`_orm.contains_eager` のようなEagerローディング機能を、ここに示すよりも深くネストされたクエリで使用しようとする場合にはそうです。このパターンは、より複雑なシナリオでは信頼できず、予測や追跡が困難な暗黙の意思決定を伴うため、警告が表示され、このパターンはレガシー機能と見なされる可能性があります。この問い合わせを書くためのより良い方法は、他の自己参照関係に適用されるものと同じパターンを使うことです。つまり、 :func:`_orm.aliased` 構文を明示的に使うことです。結合継承やその他の結合指向のマッピングでは、通常、 :paramref:`_orm.aliased.flat` パラメータの使用を追加することが望まれます。これにより、結合を新しい副問い合わせに埋め込むのではなく、結合内の個々のテーブルにエイリアスを適用することで、2つ以上のテーブルのJOINにエイリアスを適用できます:

.. sourcecode:: pycon+sql

    >>> from sqlalchemy.orm import aliased
    >>> manager_alias = aliased(Manager, flat=True)
    >>> stmt = select(Employee, manager_alias).join(Employee.reports_to.of_type(manager_alias))
    >>> print(stmt)
    {printsql}SELECT employee.id, employee.manager_id, employee.name,
    employee.type, manager_1.id AS id_1, employee_1.id AS id_2,
    employee_1.manager_id AS manager_id_1, employee_1.name AS name_1,
    employee_1.type AS type_1
    FROM employee JOIN
    (employee AS employee_1 JOIN manager AS manager_1 ON manager_1.id = employee_1.id)
    ON manager_1.id = employee.manager_id

.. If we then wanted to use :func:`_orm.contains_eager` to populate the ``reports_to`` attribute, we refer to the alias::

:func:`_orm.contains_eager` を使って ``reports_to`` 属性を生成したい場合は、エイリアスを参照します::

    >>> stmt = (
    ...     select(Employee)
    ...     .join(Employee.reports_to.of_type(manager_alias))
    ...     .options(contains_eager(Employee.reports_to.of_type(manager_alias)))
    ... )

.. Without using the explicit :func:`_orm.aliased` object, in some more nested cases the :func:`_orm.contains_eager` option does not have enough context to know where to get its data from, in the case that the ORM is "auto-aliasing" in a very nested context.  Therefore it's best not to rely on this feature and instead keep the SQL construction as explicit as possible.

明示的な :func:`_orm.aliased` オブジェクトを使用しないと、入れ子になったいくつかのケースでは、 :func:`_orm.contains_eager` オプションは、データをどこから取得するかを知るための十分なコンテキストを持っていません。これは、ORMが非常に入れ子になったコンテキストで"auto-aliasing"している場合です。したがって、この機能に頼らず、代わりにSQL構文をできるだけ明示的にしておくことが最善です。


Object Relational Mapping
-------------------------

.. _error_isce:

IllegalStateChangeError and concurrency exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. SQLAlchemy 2.0 introduced a new system described at :ref:`change_7433`, which proactively detects concurrent methods being invoked on an individual instance of the :class:`_orm.Session` object and by extension the :class:`_asyncio.AsyncSession` proxy object.  These concurrent access calls typically, though not exclusively, would occur when a single instance of :class:`_orm.Session` is shared among multiple concurrent threads without such access being synchronized, or similarly when a single instance of :class:`_asyncio.AsyncSession` is shared among multiple concurrent tasks (such as when using a function like ``asyncio.gather()``).  These use patterns are not the appropriate use of these objects, where without the proactive warning system SQLAlchemy implements would still otherwise produce invalid state within the objects, producing hard-to-debug errors including driver-level errors on the database connections themselves.

SQLAlchemy 2.0は、 :ref:`change_7433` で説明されている新しいシステムを導入しました。これは、 :class:`_orm.Session` オブジェクトの個々のインスタンス、さらには :class:`_asyncio.AsyncSession` プロキシオブジェクトで呼び出されている並行メソッドを事前に検出します。これらの並行アクセス呼び出しは、排他的ではありませんが、通常、 :class:`_orm.Session` の単一インスタンスが、そのようなアクセスが同期されていない複数の並行スレッド間で共有されている場合、または同様に、 :class:`_asyncio.AsyncSession` の単一インスタンスが複数の並行タスク間で共有されている場合(例えば、 ``asyncio.gather()`` のような関数を使用している場合)に発生します。これらの使用パターンは、これらのオブジェクトの適切な使用ではありません。事前警告システムがなければ、SQLAlchemy実装はオブジェクト内に無効な状態を生成し、データベース接続自体にドライバレベルのエラーを含むデバッグ困難なエラーを生成します。

.. Instances of :class:`_orm.Session` and :class:`_asyncio.AsyncSession` are **mutable, stateful objects with no built-in synchronization** of method calls, and represent a **single, ongoing database transaction** upon a single database connection at a time for a particular :class:`.Engine` or :class:`.AsyncEngine` to which the object is bound (note that these objects both support being bound to multiple engines at once, however in this case there will still be only one connection per engine in play within the scope of a transaction).  A single database transaction is not an appropriate target for concurrent SQL commands; instead, an application that runs concurrent database operations should use concurrent transactions. For these objects then it follows that the appropriate pattern is :class:`_orm.Session` per thread, or :class:`_asyncio.AsyncSession` per task.

:class:`_orm.Session` と :class:`_asyncio.AsyncSession` のインスタンスは、メソッド呼び出しの同期 **が組み込まれていない** 可変のステートフルなオブジェクトであり、オブジェクトがバインドされている特定の :class:`.Engine` または :class:`.AsyncEngine` に対する一度に1つのデータベース接続で、 **単一の進行中のデータベーストランザクション** を表します(これらのオブジェクトは両方とも同時に複数のエンジンにバインドすることをサポートしていますが、この場合、トランザクションのスコープ内で動作するエンジンごとに1つの接続しかありません)。単一のデータベーストランザクションは、並行SQLコマンドの適切なターゲットではありません。代わりに、並行データベース操作を実行するアプリケーションは並行トランザクションを使用する必要があります。これらのオブジェクトの場合、適切なパターンはスレッドごとの :class:`_orm.Session` か、タスクごとの :class:`_asyncio.AsyncSession` になります。

.. For more background on concurrency see the section :ref:`session_faq_threadsafe`.

並行性のバックグラウンドについては :ref:`session_faq_threadsafe` の節を参照してください。

.. _error_bhk3:

Parent instance <x> is not bound to a Session; (lazy load/deferred load/refresh/etc.) operation cannot proceed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This is likely the most common error message when dealing with the ORM, and it occurs as a result of the nature of a technique the ORM makes wide use of known as :term:`lazy loading`.   Lazy loading is a common object-relational pattern whereby an object that's persisted by the ORM maintains a proxy to the database itself, such that when various attributes upon the object are accessed, their value may be retrieved from the database *lazily*.   The advantage to this approach is that objects can be retrieved from the database without having to load all of their attributes or related data at once, and instead only that data which is requested can be delivered at that time.   The major disadvantage is basically a mirror image of the advantage, which is that if lots of objects are being loaded which are known to require a certain set of data in all cases, it is wasteful to load that additional data piecemeal.

これはORMを扱うときに最も一般的なエラーメッセージであり、ORMが広く使用している :term:`lazy loading` として知られるテクニックの性質の結果として発生します。遅延読み込みは、ORMによって永続化されたオブジェクトがデータベース自体へのプロキシを維持する一般的なオブジェクトリレーショナルパターンであり、オブジェクト上のさまざまな属性がアクセスされると、それらの値がデータベースから *遅延* して取得されます。このアプローチの利点は、すべての属性または関連データを一度にロードすることなくオブジェクトをデータベースから取得でき、代わりに要求されたデータのみをその時点で配信できることです。主な欠点は、基本的に利点の反対であり、すべての場合に特定のデータセットを必要とすることが知られている多くのオブジェクトがロードされている場合、その追加データを断片的にロードするのは無駄であるということです。

.. Another caveat of lazy loading beyond the usual efficiency concerns is that in order for lazy loading to proceed, the object has to **remain associated with a Session** in order to be able to retrieve its state.  This error message means that an object has become de-associated with its :class:`.Session` and is being asked to lazy load data from the database.

通常の効率性の問題を超えた遅延読み込みのもう1つの注意事項は、遅延読み込みが進行するためには、オブジェクトがその状態を取得できるように、 **セッションに関連付けられたまま** でなければならないことです。このエラーメッセージは、オブジェクトがその :class:`.Session` との関連付けが解除され、データベースからデータを遅延読み込みするように要求されていることを示します。

.. The most common reason that objects become detached from their :class:`.Session` is that the session itself was closed, typically via the :meth:`.Session.close` method.   The objects will then live on to be accessed further, very often within web applications where they are delivered to a server-side templating engine and are asked for further attributes which they cannot load.

オブジェクトが :class:`.Session` から切り離される最も一般的な理由は、セッション自体が、通常は :meth:`.Session.close` メソッドによって閉じられたことです。その後、オブジェクトはさらにアクセスされるために存続します。多くの場合、オブジェクトはWebアプリケーション内でサーバ側のテンプレートエンジンに配信され、ロードできない追加の属性が要求されます。

.. Mitigation of this error is via these techniques:

このエラーを軽減するには、次のテクニックを使用します。

.. * **Try not to have detached objects; don't close the session prematurely** - Often, applications will close out a transaction before passing off related objects to some other system which then fails due to this error.   Sometimes the transaction doesn't need to be closed so soon; an example is the web application closes out the transaction before the view is rendered.  This is often done in the name of "correctness", but may be seen as a mis-application of "encapsulation", as this term refers to code organization, not actual actions. The template that uses an ORM object is making use of the `proxy pattern <https://en.wikipedia.org/wiki/Proxy_pattern>`_ which keeps database logic encapsulated from the caller.   If the :class:`.Session` can be held open until the lifespan of the objects are done, this is the best approach.

* **デタッチされたオブジェクトを持たないようにしてください。セッションを早めに閉じないでください** - 多くの場合、アプリケーションは、このエラーのために失敗する他のシステムに関連するオブジェクトを渡す前に、トランザクションを閉じます。トランザクションをすぐに閉じる必要がない場合もあります。たとえば、Webアプリケーションは、ビューがレンダリングされる前にトランザクションを閉じます。これはしばしば「正当性」という名前で行われますが、この用語は実際のアクションではなくコード編成を指すため、「カプセル化」の誤った適用と見なされることがあります。ORMオブジェクトを使用するテンプレートは、呼び出し元からデータベースロジックをカプセル化したままにする `proxy pattern <https://en.wikipedia.org/wiki/Proxy_pattern>`_ を使用しています。オブジェクトのライフスパンが完了するまで :class:`.Session` を開いたままにできる場合、これが最善のアプローチです。

.. * **Otherwise, load everything that's needed up front** - It is very often impossible to keep the transaction open, especially in more complex applications that need to pass objects off to other systems that can't run in the same context even though they're in the same process.  In this case, the application should prepare to deal with :term:`detached` objects, and should try to make appropriate use of :term:`eager loading` to ensure that objects have what they need up front.

* **そうでない場合は、必要なものをすべて事前にロードしてください** - トランザクションを開いたままにしておくことは、特に、同じプロセス内にあっても同じコンテキストで実行できない他のシステムにオブジェクトを渡す必要がある、より複雑なアプリケーションでは、非常に多くの場合不可能です。この場合、アプリケーションは :term:`detached` オブジェクトを処理する準備をし、 :term:`eager loading` を適切に使用して、オブジェクトが事前に必要なものを持っていることを確認する必要があります。

.. * **And importantly, set expire_on_commit to False** - When using detached objects, the most common reason objects need to re-load data is because they were expired from the last call to :meth:`_orm.Session.commit`.   This expiration should not be used when dealing with detached objects; so the :paramref:`_orm.Session.expire_on_commit` parameter be set to ``False``.  By preventing the objects from becoming expired outside of the transaction, the data which was loaded will remain present and will not incur additional lazy loads when that data is accessed.

* **そして重要なのは、expire_on_commitをFalseに設定することです** - デタッチされたオブジェクトを使用する場合、オブジェクトがデータを再ロードする必要がある最も一般的な理由は、オブジェクトが :meth:`_orm.Session.commit` の最後の呼び出しから期限切れになっているためです。この期限切れはデタッチされたオブジェクトを扱うときには使用すべきではありません。そのため、 :paramref:`_orm.Session.expire_on_commit` パラメータを ``False`` に設定します。オブジェクトがトランザクションの外部で期限切れにならないようにすることで、ロードされたデータはそのまま残り、そのデータにアクセスしたときに追加の遅延ロードが発生することはありません。

..   Note also that :meth:`_orm.Session.rollback` method unconditionally expires all contents in the :class:`_orm.Session` and should also be avoided in non-error scenarios.

  :meth:`_orm.Session.rollback` メソッドは :class:`_orm.Session` 内のすべての内容を無条件に期限切れにすることにも注意してください。また、エラーのないシナリオでは避けるべきです。

  .. seealso::

    .. :ref:`loading_toplevel` - detailed documentation on eager loading and other relationship-oriented loading techniques

    :ref:`loading_toplevel` - Eager Loadingやその他のRelationship-Oriented Loadingテクニックに関する詳細なドキュメント

    .. :ref:`session_committing` - background on session commit

    :ref:`session_committing` - セッションのコミットのバックグラウンド

    .. :ref:`session_expire` - background on attribute expiry

    :ref:`session_expire` - 属性の有効期限のバックグラウンド


.. _error_7s2a:

This Session's transaction has been rolled back due to a previous exception during flush
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The flush process of the :class:`.Session`, described at :ref:`session_flushing`, will roll back the database transaction if an error is encountered, in order to maintain internal consistency.  However, once this occurs, the session's transaction is now "inactive" and must be explicitly rolled back by the calling application, in the same way that it would otherwise need to be explicitly committed if a failure had not occurred.

:ref:`session_flushing` で説明されている :class:`.Session` のフラッシュプロセスは、エラーが発生した場合、内部の一貫性を維持するためにデータベーストランザクションをロールバックします。しかし、これが発生すると、セッションのトランザクションは「非アクティブ」になり、失敗が発生しなかった場合に明示的にコミットする必要があるのと同じ方法で、呼び出し側アプリケーションによって明示的にロールバックする必要があります。

.. This is a common error when using the ORM and typically applies to an application that doesn't yet have correct "framing" around its :class:`.Session` operations. Further detail is described in the FAQ at :ref:`faq_session_rollback`.

これはORMを使うときによくあるエラーで、通常は :class:`.Session` 操作の周りに正しい"枠組み"がないアプリケーションに当てはまります。詳細は :ref:`faq_session_rollback` のFAQで説明されています。

.. _error_bbf0:

For relationship <relationship>, delete-orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This error arises when the "delete-orphan" :ref:`cascade <unitofwork_cascades>` is set on a many-to-one or many-to-many relationship, such as::

このエラーは、"delete-orphan" :ref:`cascade <unitofwork_cascades>` が以下のような多対1または多対多の関係に設定されている場合に発生します::

    class A(Base):
        __tablename__ = "a"

        id = Column(Integer, primary_key=True)

        bs = relationship("B", back_populates="a")


    class B(Base):
        __tablename__ = "b"
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey("a.id"))

        # this will emit the error message when the mapper
        # configuration step occurs
        a = relationship("A", back_populates="bs", cascade="all, delete-orphan")


    configure_mappers()

.. Above, the "delete-orphan" setting on ``B.a`` indicates the intent that when every ``B`` object that refers to a particular ``A`` is deleted, that the ``A`` should then be deleted as well.   That is, it expresses that the "orphan" which is being deleted would be an ``A`` object, and it becomes an "orphan" when every ``B`` that refers to it is deleted.

上記の ``B.a`` の"delete-orphan"設定は、特定の ``A`` を参照するすべての ``B`` オブジェクトが削除された場合、 ``A`` も削除されるべきであるという意図を示しています。つまり、削除される"orphan"は ``A`` オブジェクトであり、それを参照するすべての ``B`` が削除されると"orphan"になることを表しています。

.. The "delete-orphan" cascade model does not support this functionality.   The "orphan" consideration is only made in terms of the deletion of a single object which would then refer to zero or more objects that are now "orphaned" by this single deletion, which would result in those objects being deleted as well.  In other words, it is designed only to track the creation of "orphans" based on the removal of one and only one "parent" object per orphan,  which is the natural case in a one-to-many relationship where a deletion of the object on the "one" side results in the subsequent deletion of the related items on the "many" side.

"delete-orphan"カスケードモデルでは、この機能はサポートされていません。"orphan"の考慮は、単一のオブジェクトの削除に関してのみ行われます。このオブジェクトは、この単一の削除によって"orphand"にされた0個以上のオブジェクトを参照します。その結果、これらのオブジェクトも削除されます。つまり、孤立オブジェクトごとに1つのみの"親"オブジェクトを削除することに基づいて、"orphan"の作成を追跡するように設計されています。これは、1対多の関係では自然なケースであり、"1"側のオブジェクトを削除すると、"多"側の関連アイテムも削除されます。

.. The above mapping in support of this functionality would instead place the cascade setting on the one-to-many side, which looks like::

この機能をサポートするための上記のマッピングでは、代わりにカスケード設定を1対多の側に置きます。これは次のようになります::

    class A(Base):
        __tablename__ = "a"

        id = Column(Integer, primary_key=True)

        bs = relationship("B", back_populates="a", cascade="all, delete-orphan")


    class B(Base):
        __tablename__ = "b"
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey("a.id"))

        a = relationship("A", back_populates="bs")

.. Where the intent is expressed that when an ``A`` is deleted, all of the ``B`` objects to which it refers are also deleted.

``A`` が削除されると、それが参照する ``B`` オブジェクトのすべても削除されるという意図が表明されている場合です。

.. The error message then goes on to suggest the usage of the :paramref:`_orm.relationship.single_parent` flag.    This flag may be used to enforce that a relationship which is capable of having many objects refer to a particular object will in fact have only **one** object referring to it at a time.   It is used for legacy or other less ideal database schemas where the foreign key relationships suggest a "many" collection, however in practice only one object would actually refer to a given target object at at time.  This uncommon scenario can be demonstrated in terms of the above example as follows::

次に、エラーメッセージは :paramref:`_orm.relationship.single_parent` フラグの使用法を示唆します。このフラグは、特定のオブジェクトを参照する多くのオブジェクトを持つことができる関係が、実際には一度に **1つの** オブジェクトしか参照しないことを強制するために使用できます。これは、外部キー関係が"多くの"コレクションを示唆するレガシーまたはその他のあまり理想的でないデータベーススキーマに使用されますが、実際には一度に1つのオブジェクトのみが特定のターゲットオブジェクトを参照します。このまれなシナリオは、次のように上記の例で示すことができます::

    class A(Base):
        __tablename__ = "a"

        id = Column(Integer, primary_key=True)

        bs = relationship("B", back_populates="a")


    class B(Base):
        __tablename__ = "b"
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey("a.id"))

        a = relationship(
            "A",
            back_populates="bs",
            single_parent=True,
            cascade="all, delete-orphan",
        )

.. The above configuration will then install a validator which will enforce that only one ``B`` may be associated with an ``A`` at at time, within the scope of the ``B.a`` relationship::

上記の設定は、 ``B.a`` 関係の範囲内で、一度に1つの ``B`` だけが ``A`` に関連付けられることを強制するバリデータをインストールします::



    >>> b1 = B()
    >>> b2 = B()
    >>> a1 = A()
    >>> b1.a = a1
    >>> b2.a = a1
    sqlalchemy.exc.InvalidRequestError: Instance <A at 0x7eff44359350> is
    already associated with an instance of <class '__main__.B'> via its
    B.a attribute, and is only allowed a single parent.

.. Note that this validator is of limited scope and will not prevent multiple "parents" from being created via the other direction.  For example, it will not detect the same setting in terms of ``A.bs``:

このバリデータの有効範囲は限られており、複数の"親"が別の方向から作成されるのを防ぐことはできないことに注意してください。たとえば、 ``A.bs`` に関しては同じ設定は検出されません。

.. sourcecode:: pycon+sql

    >>> a1.bs = [b1, b2]
    >>> session.add_all([a1, b1, b2])
    >>> session.commit()
    {execsql}
    INSERT INTO a DEFAULT VALUES
    ()
    INSERT INTO b (a_id) VALUES (?)
    (1,)
    INSERT INTO b (a_id) VALUES (?)
    (1,)

.. However, things will not go as expected later on, as the "delete-orphan" cascade will continue to work in terms of a **single** lead object, meaning if we delete **either** of the ``B`` objects, the ``A`` is deleted.   The other ``B`` stays around, where the ORM will usually be smart enough to set the foreign key attribute to NULL, but this is usually not what's desired:

しかし、"delete-orphan"カスケードは **単一の** リードオブジェクトに関して機能し続けるので、後で物事は期待通りに進みません。つまり、 ``B`` オブジェクトの **いずれか** を削除すると、 ``A`` が削除されます。もう1つの ``B`` は近くにあり、ORMは通常、外部キー属性をNULLに設定するのに十分な賢さを持っていますが、通常はこれは望まれていることではありません。

.. sourcecode:: pycon+sql

    >>> session.delete(b1)
    >>> session.commit()
    {execsql}
    UPDATE b SET a_id=? WHERE b.id = ?
    (None, 2)
    DELETE FROM b WHERE b.id = ?
    (1,)
    DELETE FROM a WHERE a.id = ?
    (1,)
    COMMIT

.. For all the above examples, similar logic applies to the calculus of a many-to-many relationship; if a many-to-many relationship sets single_parent=True on one side, that side can use the "delete-orphan" cascade, however this is very unlikely to be what someone actually wants as the point of a many-to-many relationship is so that there can be many objects referring to an object in either direction.

上記のすべての例で、同様のロジックが多対多関係の計算に適用されます。多対多関係の一方でsingle_parent=Trueが設定されている場合、その側で"delete-orphan"カスケードを使用できます。ただし、多対多関係のポイントは、どちらの方向にもオブジェクトを参照する多くのオブジェクトが存在できるようにすることであるため、これが実際に必要とされるものである可能性は非常に低くなります。

.. Overall, "delete-orphan" cascade is usually applied on the "one" side of a one-to-many relationship so that it deletes objects in the "many" side, and not the other way around.

全体として、 "delete-orphan"カスケードは通常、1対多関係の"1"側に適用されるため、"多"側のオブジェクトは削除されますが、その逆は行われません。

.. .. versionchanged:: 1.3.18  The text of the "delete-orphan" error message when used on a many-to-one or many-to-many relationship has been updated to be more descriptive.

.. versionchanged:: 1.3.18  多対1または多対多の関係で使用された場合の"delete-orphan"エラーメッセージのテキストが、より説明的に更新されました。

.. seealso::

    :ref:`unitofwork_cascades`

    :ref:`cascade_delete_orphan`

    :ref:`error_bbf1`

.. _error_bbf1:

Instance <instance> is already associated with an instance of <instance> via its <attribute> attribute, and is only allowed a single parent.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This error is emitted when the :paramref:`_orm.relationship.single_parent` flag is used, and more than one object is assigned as the "parent" of an object at once.

このエラーは、 :paramref:`_orm.relationship.single_parent` フラグが使用され、同時に複数のオブジェクトがオブジェクトの"親"として割り当てられた場合に発生します。

.. Given the following mapping::

次のようにマッピングします::

    class A(Base):
        __tablename__ = "a"

        id = Column(Integer, primary_key=True)


    class B(Base):
        __tablename__ = "b"
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey("a.id"))

        a = relationship(
            "A",
            single_parent=True,
            cascade="all, delete-orphan",
        )

.. The intent indicates that no more than a single ``B`` object may refer to a particular ``A`` object at once::

インテントは、特定の ``A`` オブジェクトを一度に参照できる ``B`` オブジェクトは1つだけであることを示しています::

    >>> b1 = B()
    >>> b2 = B()
    >>> a1 = A()
    >>> b1.a = a1
    >>> b2.a = a1
    sqlalchemy.exc.InvalidRequestError: Instance <A at 0x7eff44359350> is
    already associated with an instance of <class '__main__.B'> via its
    B.a attribute, and is only allowed a single parent.

.. When this error occurs unexpectedly, it is usually because the :paramref:`_orm.relationship.single_parent` flag was applied in response to the error message described at :ref:`error_bbf0`, and the issue is in fact a misunderstanding of the "delete-orphan" cascade setting.  See that message for details.

このエラーが予期せずに発生した場合、通常は :ref:`error_bbf0` で説明されているエラーメッセージに応じて :paramref:`_orm.relationship.single_parent` フラグが適用されたことが原因であり、この問題は実際には"delete-orphan"カスケード設定の誤解です。詳細については、このメッセージを参照してください。

.. seealso::

    :ref:`error_bbf0`

.. _error_qzyx:

relationship X will copy column Q to column P, which conflicts with relationship(s): 'Y'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This warning refers to the case when two or more relationships will write data to the same columns on flush, but the ORM does not have any means of coordinating these relationships together. Depending on specifics, the solution may be that two relationships need to be referenced by one another using :paramref:`_orm.relationship.back_populates`, or that one or more of the relationships should be configured with :paramref:`_orm.relationship.viewonly` to prevent conflicting writes, or sometimes that the configuration is fully intentional and should configure :paramref:`_orm.relationship.overlaps` to silence each warning.

この警告は、2つ以上の関係がフラッシュ時に同じ列にデータを書き込むが、ORMにはこれらの関係を調整する手段がない場合を指します。具体的には、 :paramref:`_orm.relationship.back_populates` を使用して2つの関係を互いに参照する必要がある、1つ以上の関係を :paramref:`_orm.relationship.viewonly` で設定して書き込みの競合を防ぐ、場合によっては設定が完全に意図的であり、 :paramref:`_orm.relationship.overlaps` を設定して各警告を沈黙させる、などの解決策が考えられます。

.. For the typical example that's missing :paramref:`_orm.relationship.back_populates`, given the following mapping::

:paramref:`_orm.relationship.back_populates` が欠落している典型的な例では、次のようにマッピングされます::

    class Parent(Base):
        __tablename__ = "parent"
        id = Column(Integer, primary_key=True)
        children = relationship("Child")


    class Child(Base):
        __tablename__ = "child"
        id = Column(Integer, primary_key=True)
        parent_id = Column(ForeignKey("parent.id"))
        parent = relationship("Parent")

.. The above mapping will generate warnings:

上記のマッピングでは警告が生成されます:


.. sourcecode:: text

  SAWarning: relationship 'Child.parent' will copy column parent.id to column child.parent_id,
  which conflicts with relationship(s): 'Parent.children' (copies parent.id to child.parent_id).

.. The relationships ``Child.parent`` and ``Parent.children`` appear to be in conflict.  The solution is to apply :paramref:`_orm.relationship.back_populates`::

``Child.parent`` と ``Parent.children`` の関係が矛盾しているようです。解決策は :paramref:`_orm.relationship.back_populates` を適用することです::

    class Parent(Base):
        __tablename__ = "parent"
        id = Column(Integer, primary_key=True)
        children = relationship("Child", back_populates="parent")


    class Child(Base):
        __tablename__ = "child"
        id = Column(Integer, primary_key=True)
        parent_id = Column(ForeignKey("parent.id"))
        parent = relationship("Parent", back_populates="children")

.. For more customized relationships where an "overlap" situation may be intentional and cannot be resolved, the :paramref:`_orm.relationship.overlaps` parameter may specify the names of relationships for which the warning should not take effect. This typically occurs for two or more relationships to the same underlying table that include custom :paramref:`_orm.relationship.primaryjoin` conditions that limit the related items in each case::

"オーバーラップ"状態が意図的で解決できない、よりカスタマイズされた関係の場合、 :paramref:`_orm.relationship.overlaps` パラメータは、警告が有効にならない関係の名前を指定することがあります。これは通常、それぞれのケースで関連する項目を制限するカスタムの :paramref:`_orm.relationship.primaryjoin` 条件を含む、同じ基礎となるテーブルに対する2つ以上の関係に対して発生します::

    class Parent(Base):
        __tablename__ = "parent"
        id = Column(Integer, primary_key=True)
        c1 = relationship(
            "Child",
            primaryjoin="and_(Parent.id == Child.parent_id, Child.flag == 0)",
            backref="parent",
            overlaps="c2, parent",
        )
        c2 = relationship(
            "Child",
            primaryjoin="and_(Parent.id == Child.parent_id, Child.flag == 1)",
            overlaps="c1, parent",
        )


    class Child(Base):
        __tablename__ = "child"
        id = Column(Integer, primary_key=True)
        parent_id = Column(ForeignKey("parent.id"))

        flag = Column(Integer)

.. Above, the ORM will know that the overlap between ``Parent.c1``, ``Parent.c2`` and ``Child.parent`` is intentional.

上記では、ORMは ``Parent.c1`` 、 ``Parent.c2`` 、 ``Child.parent`` の間の重複が意図的であることを認識します。

.. _error_lkrp:

Object cannot be converted to 'persistent' state, as this identity map is no longer valid.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.4.26

.. This message was added to accommodate for the case where a :class:`_result.Result` object that would yield ORM objects is iterated after the originating :class:`_orm.Session` has been closed, or otherwise had its :meth:`_orm.Session.expunge_all` method called. When a :class:`_orm.Session` expunges all objects at once, the internal :term:`identity map` used by that :class:`_orm.Session` is replaced with a new one, and the original one discarded. An unconsumed and unbuffered :class:`_result.Result` object will internally maintain a reference to that now-discarded identity map. Therefore, when the :class:`_result.Result` is consumed, the objects that would be yielded cannot be associated with that :class:`_orm.Session`. This arrangement is by design as it is generally not recommended to iterate an unbuffered :class:`_result.Result` object outside of the transactional context in which it was created::

このメッセージは、ORMオブジェクトを生成する :class:`_result.Result` オブジェクトが、元の :class:`_orm.Session` が閉じられた後、またはその :meth:`_orm.Session.expunge_all` メソッドが呼び出された後に繰り返される場合に対応するために追加されました。 :class:`_orm.Session` が一度にすべてのオブジェクトを削除すると、その :class:`_orm.Session` で使用されている内部の :term:`identity map` は新しいものに置き換えられ、元のものは破棄されます。消費されず、バッファもされていない :class:`_result.Result` オブジェクトは、破棄されたidentity mapへの参照を内部で保持します。したがって、 :class:`_result.Result` が消費されると、生成されるオブジェクトをその :class:`_orm.Session` に関連付けることはできません。一般に、バッファもされていない :class:`_result.Result` オブジェクトを、それが作成されたトランザクションコンテキストの外で繰り返すことは推奨されないので、この配置は設計上のものです::

    # context manager creates new Session
    with Session(engine) as session_obj:
        result = sess.execute(select(User).where(User.id == 7))

    # context manager is closed, so session_obj above is closed, identity
    # map is replaced

    # iterating the result object can't associate the object with the
    # Session, raises this error.
    user = result.first()

.. The above situation typically will **not** occur when using the ``asyncio`` ORM extension, as when :class:`.AsyncSession` returns a sync-style :class:`_result.Result`, the results have been pre-buffered when the statement was executed.  This is to allow secondary eager loaders to invoke without needing an additional ``await`` call.

上記の状況は、 :class:`.AsyncSession` がsync-styleの :class:`_result.Result` を返す場合のように、ORM拡張の ``asyncio`` を使用する場合には **発生しません** 。この場合、結果は文の実行時に事前にバッファされています。これは、2番目のEager Loaderが追加の ``await`` 呼び出しを必要とせずに呼び出すことを可能にするためです。

.. To pre-buffer results in the above situation using the regular :class:`_orm.Session` in the same way that the ``asyncio`` extension does it, the ``prebuffer_rows`` execution option may be used as follows::

上記の状況で、通常の :class:`_orm.Session` を使って、 ``asyncio`` 拡張が行うのと同じように結果を事前にバッファリングするには、次のように ``prebuffer_rows`` 実行オプションを使うことができます::

    # context manager creates new Session
    with Session(engine) as session_obj:
        # result internally pre-fetches all objects
        result = sess.execute(
            select(User).where(User.id == 7), execution_options={"prebuffer_rows": True}
        )

    # context manager is closed, so session_obj above is closed, identity
    # map is replaced

    # pre-buffered objects are returned
    user = result.first()

    # however they are detached from the session, which has been closed
    assert inspect(user).detached
    assert inspect(user).session is None

.. Above, the selected ORM objects are fully generated within the ``session_obj`` block, associated with ``session_obj`` and buffered within the :class:`_result.Result` object for iteration. Outside the block, ``session_obj`` is closed and expunges these ORM objects. Iterating the :class:`_result.Result` object will yield those ORM objects, however as their originating :class:`_orm.Session` has expunged them, they will be delivered in the :term:`detached` state.

上の例では、選択されたORMオブジェクトは完全に ``session_obj`` ブロック内で生成され、 ``session_obj`` に関連付けられ、 :class:`_result.Result` オブジェクト内に反復のためにバッファされます。ブロックの外では、 ``session_obj`` が閉じられ、これらのORMオブジェクトが削除されます。 :class:`_result.Result` オブジェクトを反復すると、これらのORMオブジェクトが生成されますが、元の :class:`_orm.Session` がそれらを削除すると、それらは :term:`detached` 状態で配信されます。

.. .. note:: The above reference to a "pre-buffered" vs. "un-buffered" :class:`_result.Result` object refers to the process by which the ORM converts incoming raw database rows from the :term:`DBAPI` into ORM objects.  It does not imply whether or not the underlying ``cursor`` object itself, which represents pending results from the DBAPI, is itself buffered or unbuffered, as this is essentially a lower layer of buffering.  For background on buffering of the ``cursor`` results itself, see the section :ref:`engine_stream_results`.

.. note:: 上記の"pre-buffered"対"un-buffered" :class:`_result.Result` オブジェクトへの参照は、ORMが :term:`DBAPI` から入ってくる生のデータベース行をORMオブジェクトに変換するプロセスを参照しています。これは、DBAPIからの保留中の結果を表す基礎となる ``cursor`` オブジェクト自体が、本質的にはバッファリングの下位層であるため、バッファリングされているか、されていないかを意味するものではありません。 ``cursor`` 結果自体のバッファリングのバックグラウンドについては、 :ref:`engine_stream_results` のセクションを参照してください。



.. _error_zlpr:

Type annotation can't be interpreted for Annotated Declarative Table form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. SQLAlchemy 2.0 introduces a new :ref:`Annotated Declarative Table <orm_declarative_mapped_column>` declarative system which derives ORM mapped attribute information from :pep:`484` annotations within class definitions at runtime. A requirement of this form is that all ORM annotations must make use of a generic container called :class:`_orm.Mapped` to be properly annotated. Legacy SQLAlchemy mappings which include explicit :pep:`484` typing annotations, such as those which use the :ref:`legacy Mypy extension <mypy_toplevel>` for typing support, may include directives such as those for :func:`_orm.relationship` that don't include this generic.

SQLAlchemy 2.0では、新しい :ref:`Annotated Declarative Table <orm_declarative_mapped_column>` 宣言システムが導入されました。これは、実行時にクラス定義内の :pep:`484` アノテーションからORMにマッピングされた属性情報を導出します。この形式の要件は、すべてのORMアノテーションが適切にアノテーションされるために :class:`_orm.Mapped` と呼ばれる汎用コンテナを利用しなければならないことです。明示的な :pep:`484` 型付けアノテーションを含むレガシーSQLAlchemyマッピング(型付けサポートに :ref:`legacy Mypy extension <mypy_toplevel>` を使用するものなど)には、この汎用を含まない :func:`_orm.relationship` などのディレクティブが含まれる場合があります。

.. To resolve, the classes may be marked with the ``__allow_unmapped__`` boolean attribute until they can be fully migrated to the 2.0 syntax. See the migration notes at :ref:`migration_20_step_six` for an example.

解決するには、2.0構文に完全に移行できるようになるまで、クラスに ``__allow_unmapped__`` ブール属性を付けます。例については、 :ref:`migration_20_step_six` の移行に関する注意を参照してください。

.. seealso::

    :ref:`migration_20_step_six` - in the :ref:`migration_20_toplevel` document

.. _error_dcmx:

When transforming <cls> to a dataclass, attribute(s) originate from superclass <cls> which is not a dataclass.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This warning occurs when using the SQLAlchemy ORM Mapped Dataclasses feature described at :ref:`orm_declarative_native_dataclasses` in conjunction with any mixin class or abstract base that is not itself declared as a dataclass, such as in the example below::

この警告は、以下の例のように、 :ref:`orm_declarative_native_dataclasses` で説明されているSQLAlchemy ORM Mapped Dataclasses機能を、それ自体がデータクラスとして宣言されていないミックスインクラスまたは抽象ベースと組み合わせて使用すると発生します::

    from __future__ import annotations

    import inspect
    from typing import Optional
    from uuid import uuid4

    from sqlalchemy import String
    from sqlalchemy.orm import DeclarativeBase
    from sqlalchemy.orm import Mapped
    from sqlalchemy.orm import mapped_column
    from sqlalchemy.orm import MappedAsDataclass


    class Mixin:
        create_user: Mapped[int] = mapped_column()
        update_user: Mapped[Optional[int]] = mapped_column(default=None, init=False)


    class Base(DeclarativeBase, MappedAsDataclass):
        pass


    class User(Base, Mixin):
        __tablename__ = "sys_user"

        uid: Mapped[str] = mapped_column(
            String(50), init=False, default_factory=uuid4, primary_key=True
        )
        username: Mapped[str] = mapped_column()
        email: Mapped[str] = mapped_column()

.. Above, since ``Mixin`` does not itself extend from :class:`_orm.MappedAsDataclass`, the following warning is generated:

上記では、 ``Mixin`` 自体は :class:`_orm.MappedAsDataclass` から拡張されていないので、以下の警告が生成されます。

.. sourcecode:: none

    SADeprecationWarning: When transforming <class '__main__.User'> to a
    dataclass, attribute(s) "create_user", "update_user" originates from
    superclass <class
    '__main__.Mixin'>, which is not a dataclass. This usage is deprecated and
    will raise an error in SQLAlchemy 2.1. When declaring SQLAlchemy
    Declarative Dataclasses, ensure that all mixin classes and other
    superclasses which include attributes are also a subclass of
    MappedAsDataclass.

.. The fix is to add :class:`_orm.MappedAsDataclass` to the signature of ``Mixin`` as well::

この問題を解決するには、 :class:`_orm.MappedAsDataclass` を ``Mixin`` のシグネチャに追加します::

    class Mixin(MappedAsDataclass):
        create_user: Mapped[int] = mapped_column()
        update_user: Mapped[Optional[int]] = mapped_column(default=None, init=False)

.. Python's :pep:`681` specification does not accommodate for attributes declared on superclasses of dataclasses that are not themselves dataclasses; per the behavior of Python dataclasses, such fields are ignored, as in the following example::

Pythonの :pep:`681` 仕様は、自身がデータクラスではないデータクラスのスーパークラスで宣言された属性に対応していません。Pythonのデータクラスの動作では、以下の例のように、そのようなフィールドは無視されます::

    from dataclasses import dataclass
    from dataclasses import field
    import inspect
    from typing import Optional
    from uuid import uuid4


    class Mixin:
        create_user: int
        update_user: Optional[int] = field(default=None)


    @dataclass
    class User(Mixin):
        uid: str = field(init=False, default_factory=lambda: str(uuid4()))
        username: str
        password: str
        email: str

.. Above, the ``User`` class will not include ``create_user`` in its constructor nor will it attempt to interpret ``update_user`` as a dataclass attribute.  This is because ``Mixin`` is not a dataclass.

上記では、 ``User`` クラスはコンストラクタに ``create_user`` を含まず、 ``update_user`` をデータクラス属性として解釈しません。これは ``Mixin`` がデータクラスではないからです。

.. SQLAlchemy's dataclasses feature within the 2.0 series does not honor this behavior correctly; instead, attributes on non-dataclass mixins and superclasses are treated as part of the final dataclass configuration.  However type checkers such as Pyright and Mypy will not consider these fields as part of the dataclass constructor as they are to be ignored per :pep:`681`.  Since their presence is ambiguous otherwise, SQLAlchemy 2.1 will require that mixin classes which have SQLAlchemy mapped attributes within a dataclass hierarchy have to themselves be dataclasses.

2.0シリーズのSQLAlchemyのデータクラス機能では、この動作は正しく行われません。代わりに、非データクラスのミックスインやスーパークラスの属性は、最終的なデータクラス設定の一部として扱われます。しかし、PyrightやMypyのような型チェッカーは、これらのフィールドをデータクラスコンストラクタの一部とはみなしません。なぜなら、これらは :pep:`681` によって無視されるからです。これらの存在は他の点では曖昧であるため、SQLAlchemy 2.1では、データクラス階層内にSQLAlchemyがマップされた属性を持つミックスインクラスは、それ自体がデータクラスでなければならないことが要求されます。

.. _error_dcte:

Python dataclasses error encountered when creating dataclass for <classname>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. When using the :class:`_orm.MappedAsDataclass` mixin class or :meth:`_orm.registry.mapped_as_dataclass` decorator, SQLAlchemy makes use of the actual `Python dataclasses <dataclasses_>`_ module that's in the Python standard library in order to apply dataclass behaviors to the target class.   This API has its own error scenarios, most of which involve the construction of an ``__init__()`` method on the user defined class; the order of attributes declared on the class, as well as `on superclasses <dc_superclass_>`_, determines how the ``__init__()`` method will be constructed and there are specific rules in how the attributes are organized as well as how they should make use of parameters such as ``init=False``, ``kw_only=True``, etc.   **SQLAlchemy does not control or implement these rules**.  Therefore, for errors of this nature, consult the `Python dataclasses <dataclasses_>`_ documentation, with special attention to the rules applied to `inheritance <dc_superclass_>`_.

:class:`_orm.MappedAsDataclass` ミックスインクラスまたは :meth:`_orm.registry.mapped_as_dataclass` デコレータを使用する場合、SQLAlchemyはPython標準ライブラリにある実際の `Python dataclasses <dataclasses_>`_ モジュールを使用して、データクラスの動作をターゲットクラスに適用します。このAPIには独自のエラーシナリオがあり、そのほとんどはユーザ定義クラスでの ``__init__()`` メソッドの構築を含みます。クラスで宣言された属性の順序は、 `on superclasses <dc_superclass_>`_ と同様に、どのように ``__init__()`` メソッドが構築されるかを決定します。また、属性の編成方法や、``init=False`` 、``kw_only=True`` などのパラメータの使用方法には特定の規則があります。 **SQLAlchemyはこれらの規則を制御または実装しません** 。したがって、この種のエラーについては、 `Python dataclasses <dataclasses_>`_ のドキュメントを参照してください。特に `inheritance <dc_superclass_>`_ に適用される規則に注意してください。

.. seealso::

  .. :ref:`orm_declarative_native_dataclasses` - SQLAlchemy dataclasses documentation

  :ref:`orm_declarative_native_dataclasses` - SQLAlchemyデータクラスのドキュメント

  .. `Python dataclasses <dataclasses_>`_ - on the python.org website

  `Python dataclasses <dataclasses_>`_ - python.orgのWebサイト

  .. `inheritance <dc_superclass_>`_ - on the python.org website

  `inheritance <dc_superclass_>`_  - python.orgのWebサイト

.. _dataclasses: https://docs.python.org/3/library/dataclasses.html

.. _dc_superclass: https://docs.python.org/3/library/dataclasses.html#inheritance


.. _error_bupq:

per-row ORM Bulk Update by Primary Key requires that records contain primary key values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This error occurs when making use of the :ref:`orm_queryguide_bulk_update` feature without supplying primary key values in the given records, such as::

このエラーは、 :ref:`orm_queryguide_bulk_update` 機能を利用する際に、以下のような指定されたレコードに主キー値を指定しないと発生します::

    >>> session.execute(
    ...     update(User).where(User.name == bindparam("u_name")),
    ...     [
    ...         {"u_name": "spongebob", "fullname": "Spongebob Squarepants"},
    ...         {"u_name": "patrick", "fullname": "Patrick Star"},
    ...     ],
    ... )

.. Above, the presence of a list of parameter dictionaries combined with usage of the :class:`_orm.Session` to execute an ORM-enabled UPDATE statement will automatically make use of ORM Bulk Update by Primary Key, which expects parameter dictionaries to include primary key values, e.g.::

上記では、パラメータ辞書のリストの存在と、ORM対応のUPDATE文を実行するための :class:`_orm.Session` の使用を組み合わせることで、自動的に主キーによるORMのバルクアップデートが使用されます。これは、パラメータ辞書が主キーの値を含むことを期待しています。例えば::

    >>> session.execute(
    ...     update(User),
    ...     [
    ...         {"id": 1, "fullname": "Spongebob Squarepants"},
    ...         {"id": 3, "fullname": "Patrick Star"},
    ...         {"id": 5, "fullname": "Eugene H. Krabs"},
    ...     ],
    ... )

.. To invoke the UPDATE statement without supplying per-record primary key values, use :meth:`_orm.Session.connection` to acquire the current :class:`_engine.Connection`, then invoke with that::

レコードごとの主キーの値を指定せずにUPDATE文を呼び出すには、 :meth:`_orm.Session.connection` を使って現在の :class:`_engine.Connection` を取得し、それを使ってを呼び出します::

    >>> session.connection().execute(
    ...     update(User).where(User.name == bindparam("u_name")),
    ...     [
    ...         {"u_name": "spongebob", "fullname": "Spongebob Squarepants"},
    ...         {"u_name": "patrick", "fullname": "Patrick Star"},
    ...     ],
    ... )


.. seealso::

        :ref:`orm_queryguide_bulk_update`

        :ref:`orm_queryguide_bulk_update_disabling`



AsyncIO Exceptions
------------------

.. _error_xd1r:

AwaitRequired
~~~~~~~~~~~~~

.. The SQLAlchemy async mode requires an async driver to be used to connect to the db.  This error is usually raised when trying to use the async version of SQLAlchemy with a non compatible :term:`DBAPI`.

SQLAlchemy非同期モードでは、データベースへの接続に非同期ドライバを使用する必要があります。このエラーは通常、互換性のない :term:`DBAPI` で非同期バージョンのSQLAlchemyを使用しようとしたときに発生します。

.. seealso::

    :ref:`asyncio_toplevel`

.. _error_xd2s:

MissingGreenlet
~~~~~~~~~~~~~~~

.. A call to the async :term:`DBAPI` was initiated outside the greenlet spawn context usually setup by the SQLAlchemy AsyncIO proxy classes. Usually this error happens when an IO was attempted in an unexpected place, using a calling pattern that does not directly provide for use of the ``await`` keyword.  When using the ORM this is nearly always due to the use of :term:`lazy loading`, which is not directly supported under asyncio without additional steps and/or alternate loader patterns in order to use successfully.

async :term:`DBAPI` の呼び出しが、通常はSQLAlchemy AsyncIOプロキシクラスによって設定されたgreenlet spawnコンテキストの外で開始されました。通常、このエラーは、 ``await`` キーワードの使用を直接提供しない呼び出しパターンを使用して、予期しない場所でIOが試行されたときに発生します。ORMを使用する場合、これはほとんど常に :term:`lazy loading` の使用によるものです。これは、正常に使用するために追加のステップや代替のローダーパターンがなければ、AsyncIOで直接サポートされません。

.. seealso::

    .. :ref:`asyncio_orm_avoid_lazyloads` - covers most ORM scenarios where this problem can occur and how to mitigate, including specific patterns to use with lazy load scenarios.

    :ref:`asyncio_orm_avoid_lazyloads` - この問題が発生する可能性のあるほとんどのORMシナリオと、遅延ロードシナリオで使用する特定のパターンを含む緩和方法をカバーしています。



.. _error_xd3s:

No Inspection Available
~~~~~~~~~~~~~~~~~~~~~~~

.. Using the :func:`_sa.inspect` function directly on an :class:`_asyncio.AsyncConnection` or :class:`_asyncio.AsyncEngine` object is not currently supported, as there is not yet an awaitable form of the :class:`_reflection.Inspector` object available. Instead, the object is used by acquiring it using the :func:`_sa.inspect` function in such a way that it refers to the underlying :attr:`_asyncio.AsyncConnection.sync_connection` attribute of the :class:`_asyncio.AsyncConnection` object; the :class:`_engine.Inspector` is then used in a "synchronous" calling style by using the :meth:`_asyncio.AsyncConnection.run_sync` method along with a custom function that performs the desired operations::

:class:`_asyncio.AsyncConnection` または :class:`_asyncio.AsyncEngine` オブジェクトに対して :func:`_sa.inspect` 関数を直接使用することは、現在サポートされていません。これは、 :class:`_reflection.Inspector` オブジェクトの待機可能な形式がまだ存在しないためです。代わりに、 :class:`_asyncio.AsyncConnection` オブジェクトの基礎となる :attr:`_asyncio.AsyncConnection.sync_connection` 属性を参照するような方法で、 :func:`_sa.inspect` 関数を使用してオブジェクトを取得することによって使用されます。その後、 :class:`_engine.Inspector` は、 :meth:`_asyncio.AsyncConnection.run_sync` メソッドと、必要な操作を実行するカスタム関数を使用して、"同期"呼び出しスタイルで使用されます::

    async def async_main():
        async with engine.connect() as conn:
            tables = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )

.. seealso::

    .. :ref:`asyncio_inspector` - additional examples of using :func:`_sa.inspect` with the asyncio extension.

    :ref:`asyncio_inspector` - asyncio拡張で :func:`_sa.inspect` を使う追加の例です。

Core Exception Classes
----------------------

.. See :ref:`core_exceptions_toplevel` for Core exception classes.

コア例外クラスについては :ref:`core_exceptions_toplevel` を参照してください。


ORM Exception Classes
---------------------

.. See :ref:`orm_exceptions_toplevel` for ORM exception classes.

ORM例外クラスについては :ref:`orm_exceptions_toplevel` を参照してください。

Legacy Exceptions
-----------------

.. Exceptions in this section are not generated by current SQLAlchemy versions, however are provided here to suit exception message hyperlinks.

このセクションの例外は、現在のSQLAlchemyバージョンでは生成されませんが、例外メッセージのハイパーリンクに対応するためにここで説明します。

.. _error_b8d9:

The <some function> in SQLAlchemy 2.0 will no longer <something>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. SQLAlchemy 2.0 represents a major shift for a wide variety of key SQLAlchemy usage patterns in both the Core and ORM components.   The goal of the 2.0 release is to make a slight readjustment in some of the most fundamental assumptions of SQLAlchemy since its early beginnings, and to deliver a newly streamlined usage model that is hoped to be significantly more minimalist and consistent between the Core and ORM components, as well as more capable.

SQLAlchemy 2.0は、コアコンポーネントとORMコンポーネントの両方におけるさまざまな主要なSQLAlchemy使用パターンの大きな変化を表しています。2.0リリースの目標は、SQLAlchemyの初期の開始以来の最も基本的な前提条件のいくつかを若干再調整し、コアコンポーネントとORMコンポーネントの間で大幅にミニマムで一貫性があり、より有能であることが期待される、新たに合理化された利用モデルを提供することです。

.. Introduced at :ref:`migration_20_toplevel`, the SQLAlchemy 2.0 project includes a comprehensive future compatibility system that's integrated into the 1.4 series of SQLAlchemy, such that applications will have a clear, unambiguous, and incremental upgrade path in order to migrate applications to being fully 2.0 compatible.   The :class:`.exc.RemovedIn20Warning` deprecation warning is at the base of this system to provide guidance on what behaviors in an existing codebase will need to be modified.  An overview of how to enable this warning is at :ref:`deprecation_20_mode`.

:ref:`migration_20_toplevel` で紹介されたSQLAlchemy 2.0プロジェクトには、SQLAlchemyの1.4シリーズに統合された包括的な将来の互換性システムが含まれており、アプリケーションを完全に2.0互換に移行するために、アプリケーションに明確で曖昧さのない段階的なアップグレードパスを提供します。 :class:`.exc.RemovedIn20Warning` 非推奨警告は、既存のコードベースのどの動作を変更する必要があるかについてのガイダンスを提供するために、このシステムの基礎にあります。この警告を有効にする方法の概要は :ref:`deprecation_20_mode` にあります。

.. seealso::

    .. :ref:`migration_20_toplevel`  - An overview of the upgrade process from the 1.x series, as well as the current goals and progress of SQLAlchemy 2.0.

    :ref:`migration_20_toplevel` - 1.xシリーズからのアップグレードプロセスの概要と、SQLAlchemy 2.0の現在の目標と進捗状況。

    .. :ref:`deprecation_20_mode` - specific guidelines on how to use "2.0 deprecations mode" in SQLAlchemy 1.4.

    :ref:`deprecation_20_mode` - SQLAlchemy 1.4の"2.0 deprecations mode"の使用方法に関するガイドライン。

.. _error_s9r1:

Object is being merged into a Session along the backref cascade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This message refers to the "backref cascade" behavior of SQLAlchemy, removed in version 2.0.  This refers to the action of an object being added into a :class:`_orm.Session` as a result of another object that's already present in that session being associated with it.  As this behavior has been shown to be more confusing than helpful, the :paramref:`_orm.relationship.cascade_backrefs` and :paramref:`_orm.backref.cascade_backrefs` parameters were added, which can be set to ``False`` to disable it, and in SQLAlchemy 2.0 the "cascade backrefs" behavior has been removed entirely.

このメッセージは、バージョン2.0で削除されたSQLAlchemyの"backref cascade"の動作を参照しています。これは、そのセッションに既に存在する別のオブジェクトが関連付けられた結果として、オブジェクトが :class:`_orm.Session` に追加される動作を参照しています。この動作は役に立つというよりも混乱を招くことが示されているので、 :paramref:`_orm.relationship.cascade_backrefs` と :paramref:`_orm.backref.cascade_backrefs `パラメータが追加されました。これを ``False`` に設定して無効にすることができます。SQLAlchemy 2.0では"cascade backrefs"の動作は完全に削除されました。

.. For older SQLAlchemy versions, to set :paramref:`_orm.relationship.cascade_backrefs` to ``False`` on a backref that is currently configured using the :paramref:`_orm.relationship.backref` string parameter, the backref must be declared using the :func:`_orm.backref` function first so that the :paramref:`_orm.backref.cascade_backrefs` parameter may be passed.

古いバージョンのSQLAlchemyでは、現在 :paramref:`_orm.relationship.backref` 文字列パラメータを使って設定されているbackrefに対して :paramref:`_orm.relationship.cascade_backrefs` を ``False`` に設定するには、まず :func:`_orm.backref `関数を使ってbackrefを宣言して、: paramref:`_orm.backref.cascade_backrefs` パラメータを渡せるようにしなければなりません。

.. Alternatively, the entire "cascade backrefs" behavior can be turned off across the board by using the :class:`_orm.Session` in "future" mode, by passing ``True`` for the :paramref:`_orm.Session.future` parameter.

あるいは、 :paramref:`_orm.Session.future` パラメータに ``True`` を渡すことで、"future"モードで :class:`_orm.Session` を 使用して、"cascade backrefs"動作全体を全面的にオフにすることもできます。

.. seealso::

    .. :ref:`change_5150` - background on the change for SQLAlchemy 2.0.

    :ref:`change_5150` - SQLAlchemy 2.0の変更のバックグラウンド

.. _error_c9ae:

select() construct created in "legacy" mode; keyword arguments, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The :func:`_expression.select` construct has been updated as of SQLAlchemy 1.4 to support the newer calling style that is standard in SQLAlchemy 2.0.   For backwards compatibility within the 1.4 series, the construct accepts arguments in both the "legacy" style as well as the "new" style.

:func:`_expression.select` 構文はSQLAlchemy 1.4の時点で更新され、SQLAlchemy 2.0の標準である新しい呼び出しスタイルをサポートします。1.4シリーズとの下位互換性のために、この構文は"legacy"スタイルと"new"スタイルの両方の引数を受け付けます。

.. The "new" style features that column and table expressions are passed positionally to the :func:`_expression.select` construct only; any other modifiers to the object must be passed using subsequent method chaining::

"new"スタイルは、列とテーブルの式が :func:`_expression.select` 構文に位置的に渡されることを特徴としています。オブジェクトに対するその他の修飾子は、後続のメソッドチェーニングを使って渡さなければなりません::

    # this is the way to do it going forward
    stmt = select(table1.c.myid).where(table1.c.myid == table2.c.otherid)

.. For comparison, a :func:`_expression.select` in legacy forms of SQLAlchemy, before methods like :meth:`.Select.where` were even added, would like::

比較のために、 :meth:`.Select.where` のようなメソッドが追加される前のSQLAlchemyのレガシー形式の :func:`_expression.select` は、次のようになります::

    # this is how it was documented in original SQLAlchemy versions
    # many years ago
    stmt = select([table1.c.myid], whereclause=table1.c.myid == table2.c.otherid)

.. Or even that the "whereclause" would be passed positionally::

あるいは、"where句"が位置的に渡されることもあります::

    # this is also how it was documented in original SQLAlchemy versions
    # many years ago
    stmt = select([table1.c.myid], table1.c.myid == table2.c.otherid)

.. For some years now, the additional "whereclause" and other arguments that are accepted have been removed from most narrative documentation, leading to a calling style that is most familiar as the list of column arguments passed as a list, but no further arguments::

ここ数年、追加の"where句"やその他の引数が受け入れられていましたが、ほとんどの説明文書から削除されました。これにより、リストとして渡される列引数のリストとして最もよく知られた呼び出しスタイルになりましたが、それ以上の引数はありません::

    # this is how it's been documented since around version 1.0 or so
    stmt = select([table1.c.myid]).where(table1.c.myid == table2.c.otherid)

.. The document at :ref:`migration_20_5284` describes this change in terms of :ref:`2.0 Migration <migration_20_toplevel>`.

:ref:`migration_20_5284` の文書では、この変更を :ref:`2.0 Migration <migration_20_toplevel>` の観点から説明しています。

.. seealso::

    :ref:`migration_20_5284`

    :ref:`migration_20_toplevel`

.. _error_c9bf:

A bind was located via legacy bound metadata, but since future=True is set on this Session, this bind is ignored.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The concept of "bound metadata" is present up until SQLAlchemy 1.4; as of SQLAlchemy 2.0 it's been removed.

"バインドされたメタデータ"という概念はSQLAlchemy 1.4まで存在していましたが、SQLAlchemy 2.0では削除されました。

.. This error refers to the :paramref:`_schema.MetaData.bind` parameter on the :class:`_schema.MetaData` object that in turn allows objects like the ORM :class:`_orm.Session` to associate a particular mapped class with an :class:`_orm.Engine`. In SQLAlchemy 2.0, the :class:`_orm.Session` must be linked to each :class:`_orm.Engine` directly. That is, instead of instantiating the :class:`_orm.Session` or :class:`_orm.sessionmaker` without any arguments, and associating the :class:`_engine.Engine` with the :class:`_schema.MetaData`::

このエラーは、ORM :class:`_orm.Session` のようなオブジェクトが特定のマップされたクラスを :class:`_orm.Engine` に関連付けることを可能にする :class:`_schema.MetaData` オブジェクトの :paramref:`_schema.MetaData.bind` パラメータを参照します。SQLAlchemy 2.0では、 :class:`_orm.Session` は各 :class:`_orm.Engine` に直接リンクされていなければなりません。つまり、引数なしで :class:`_orm.Session` または :class:`_orm.sessionmaker` をインスタンス化し、 :class:`_engine.Engine` を :class:`_schema.MetaData` に関連付けるのではありません::

    engine = create_engine("sqlite://")
    Session = sessionmaker()
    metadata_obj = MetaData(bind=engine)
    Base = declarative_base(metadata=metadata_obj)


    class MyClass(Base): ...


    session = Session()
    session.add(MyClass())
    session.commit()

.. The :class:`_engine.Engine` must instead be associated directly with the :class:`_orm.sessionmaker` or :class:`_orm.Session`.  The :class:`_schema.MetaData` object should no longer be associated with any engine::

代わりに、 :class:`_engine.Engine` を :class:`_orm.sessionmaker` または :class:`_orm.Session` に直接関連付ける必要があります。 :class:`_schema.MetaData` オブジェクトはどのエンジンにも関連付けるべきではありません::

    engine = create_engine("sqlite://")
    Session = sessionmaker(engine)
    Base = declarative_base()


    class MyClass(Base): ...


    session = Session()
    session.add(MyClass())
    session.commit()

.. In SQLAlchemy 1.4, this :term:`2.0 style` behavior is enabled when the :paramref:`_orm.Session.future` flag is set on :class:`_orm.sessionmaker` or :class:`_orm.Session`.

SQLAlchemy 1.4では、この :term:`2.0 style` の振る舞いは、 :paramref:`_orm.Session.future` フラグが :class:`_orm.sessionmaker` または :class:`_orm.Session` に設定されている場合に有効になります。

.. _error_2afi:

This Compiled object is not bound to any Engine or Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This error refers to the concept of "bound metadata", which is a legacy SQLAlchemy pattern present only in 1.x versions. The issue occurs when one invokes the :meth:`.Executable.execute` method directly off of a Core expression object that is not associated with any :class:`_engine.Engine`::

このエラーは、1.xバージョンにのみ存在するレガシーSQLAlchemyパターンである"バインドされたメタデータ"の概念に関連しています。この問題は、 :class:`_engine.Engine` に関連付けられていないCore式オブジェクトから直接 :meth:`.Executable.execute` メソッドを呼び出したときに発生します::

    metadata_obj = MetaData()
    table = Table("t", metadata_obj, Column("q", Integer))

    stmt = select(table)
    result = stmt.execute()  # <--- raises

.. What the logic is expecting is that the :class:`_schema.MetaData` object has been **bound** to a :class:`_engine.Engine`::

このロジックが想定しているのは、 :class:`_schema.MetaData` オブジェクトが :class:`_engine.Engine` に **バインド** されているということです::

    engine = create_engine("mysql+pymysql://user:pass@host/db")
    metadata_obj = MetaData(bind=engine)

.. Where above, any statement that derives from a :class:`_schema.Table` which in turn derives from that :class:`_schema.MetaData` will implicitly make use of the given :class:`_engine.Engine` in order to invoke the statement.

上記の場合、 :class:`_schema.Table` から派生し、その :class:`_schema.MetaData` から派生するステートメントは、暗黙的に指定された :class:`_engine.Engine` を使用してステートメントを呼び出します。

.. Note that the concept of bound metadata is **not present in SQLAlchemy 2.0**.  The correct way to invoke statements is via the :meth:`_engine.Connection.execute` method of a :class:`_engine.Connection`::

バインドされたメタデータの概念は、 **SQLAlchemy 2.0** には存在しないことに注意してください。文を呼び出す正しい方法は、 :class:`_engine.Connection` の :meth:`_engine.Connection.execute` メソッドを使用することです::

    with engine.connect() as conn:
        result = conn.execute(stmt)

.. When using the ORM, a similar facility is available via the :class:`.Session`::

ORMを使用する場合、 :class:`.Session` 経由で同様の機能を利用できます::

    result = session.execute(stmt)

.. seealso::

    :ref:`tutorial_statement_execution`

.. _error_8s2a:

This connection is on an inactive transaction.  Please rollback() fully before proceeding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. This error condition was added to SQLAlchemy as of version 1.4, and does not apply to SQLAlchemy 2.0.    The error refers to the state where a :class:`_engine.Connection` is placed into a transaction using a method like :meth:`_engine.Connection.begin`, and then a further "marker" transaction is created within that scope; the "marker" transaction is then rolled back using :meth:`.Transaction.rollback` or closed using :meth:`.Transaction.close`, however the outer transaction is still present in an "inactive" state and must be rolled back.

このエラー条件は、バージョン1.4のSQLAlchemyに追加されたもので、SQLAlchemy 2.0には適用されません。このエラーは、 :class:`_engine.Connection` が :meth:`_engine.Connection.begin` のようなメソッドを使ってトランザクションに入れられ、そのスコープ内でさらに"マーカー"トランザクションが作成される状態を指します。"マーカー"トランザクションは、その後 :meth:`.Transaction.rollback` を使ってロールバックされるか、 :meth:`.Transaction.close` を使って閉じられますが、外側のトランザクションはまだ"非アクティブ"な状態なので、ロールバックする必要があります。

The pattern looks like::

    engine = create_engine(...)

    connection = engine.connect()
    transaction1 = connection.begin()

    # this is a "sub" or "marker" transaction, a logical nesting
    # structure based on "real" transaction transaction1
    transaction2 = connection.begin()
    transaction2.rollback()

    # transaction1 is still present and needs explicit rollback,
    # so this will raise
    connection.execute(text("select 1"))

.. Above, ``transaction2`` is a "marker" transaction, which indicates a logical nesting of transactions within an outer one; while the inner transaction can roll back the whole transaction via its rollback() method, its commit() method has no effect except to close the scope of the "marker" transaction itself.   The call to ``transaction2.rollback()`` has the effect of **deactivating** transaction1 which means it is essentially rolled back at the database level, however is still present in order to accommodate a consistent nesting pattern of transactions.

上の例では、 ``transaction2`` は ``マーカー`` トランザクションであり、外部トランザクション内の論理的なネストを示しています。内部トランザクションはrollback()メソッドによってトランザクション全体をロールバックできますが、commit()メソッドは"マーカー"トランザクション自体のスコープを閉じる以外には何の効果もありません。 ``transaction2.rollback()`` の呼び出しは、基本的にデータベースレベルでロールバックされることを意味する ``transaction1`` を **非アクティブ化** する効果がありますが、トランザクションの一貫したネストパターンに対応するために存在しています。

.. The correct resolution is to ensure the outer transaction is also rolled back::

正しい解決方法は、外部トランザクションも確実にロールバックされるようにすることです::

    transaction1.rollback()

.. This pattern is not commonly used in Core.  Within the ORM, a similar issue can occur which is the product of the ORM's "logical" transaction structure; this is described in the FAQ entry at :ref:`faq_session_rollback`.

このパターンはCoreでは一般的に使用されていません。ORM内では、ORMの "論理的な" トランザクション構造の産物である同様の問題が発生する可能性があります。これは :ref:`faq_session_rollback` のFAQエントリで説明されています。

.. The "subtransaction" pattern is removed in SQLAlchemy 2.0 so that this particular programming pattern is no longer be available, preventing this error message.

SQLAlchemy 2.0では"subtransaction"パターンが削除されたため、この特定のプログラミングパターンは使用できなくなり、このエラーメッセージが表示されなくなりました。
