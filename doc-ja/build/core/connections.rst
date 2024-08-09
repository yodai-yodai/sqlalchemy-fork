.. _connections_toplevel:

====================================
Working with Engines and Connections
====================================

.. module:: sqlalchemy.engine

.. This section details direct usage of the :class:`_engine.Engine`, :class:`_engine.Connection`, and related objects. Its important to note that when using the SQLAlchemy ORM, these objects are not generally accessed; instead, the :class:`.Session` object is used as the interface to the database.  However, for applications that are built around direct usage of textual SQL statements and/or SQL expression constructs without involvement by the ORM's higher level management services, the :class:`_engine.Engine` and :class:`_engine.Connection` are king (and queen?) - read on.

この節では、:class:`_engine.Engine` , :class:`_engine.Connection` および関連するオブジェクトの直接の使用法について詳しく説明します。SQLAlchemy ORMを使用する場合、これらのオブジェクトは一般にアクセスされないことに注意してください。代わりに、 :class:`.Session` オブジェクトがデータベースへのインタフェースとして使用されます。しかし、ORMの上位レベルの管理サービスの関与なしに、テキストのSQL文やSQL式の構成体を直接使用して構築されたアプリケーションの場合、 :class:`_engine.Engine` と :class:`_engine.Connection` はキング(そしてクイーン?)です - 続きを読んでください。

Basic Usage
-----------

.. Recall from :doc:`/core/engines` that an :class:`_engine.Engine` is created via the :func:`_sa.create_engine` call::

:doc:`/core/engines` から、 :class:`_engine.Engine` が :func:`_sa.create_engine` 呼び出しによって作成されることを思い出してください::

    engine = create_engine("mysql+mysqldb://scott:tiger@localhost/test")

.. The typical usage of :func:`_sa.create_engine` is once per particular database URL, held globally for the lifetime of a single application process. A single :class:`_engine.Engine` manages many individual :term:`DBAPI` connections on behalf of the process and is intended to be called upon in a concurrent fashion. The :class:`_engine.Engine` is **not** synonymous to the DBAPI ``connect()`` function, which represents just one connection resource - the :class:`_engine.Engine` is most efficient when created just once at the module level of an application, not per-object or per-function call.

:func:`_sa.create_engine` の一般的な使い方は、特定のデータベースURLごとに1回、単一のアプリケーションプロセスの存続期間にわたってグ行バルに保持されます。単一の :class:`_engine.Engine` は、プロセスに代わって多くの個別の :term:`DBAPI` 接続を管理し、同時に呼び出されることを意図しています。 :class:`_engine.Engine` は、ただ1つの接続リソースを表すDBAPIの ``connect()`` 関数と 同義では **ありません** 。 :class:`_engine.Engine` は、オブジェクト単位や関数単位の呼び出しではなく、アプリケーションのモジュールレベルで1回だけ作成すると最も効率的です。

.. sidebar:: tip

    .. When using an :class:`_engine.Engine` with multiple Python processes, such as when using ``os.fork`` or Python ``multiprocessing``, it's important that the engine is initialized per process.  See :ref:`pooling_multiprocessing` for details.

    複数のPythonプロセスで :class:`_engine.Engine` を使用する場合、例えば ``os.fork`` やPythonの ``multiprocessing`` を使用する場合、エンジンがプロセスごとに初期化されていることが重要です。詳細は :ref:`pooling_multiprocessing` を参照してください。

.. The most basic function of the :class:`_engine.Engine` is to provide access to a :class:`_engine.Connection`, which can then invoke SQL statements. To emit a textual statement to the database looks like::

:class:`_engine.Engine` の最も基本的な機能は、SQL文を呼び出すことができる :class:`_engine.Connection` へのアクセスを提供することです。データベースにテキスト文を出力するには、次のようにします::

    from sqlalchemy import text

    with engine.connect() as connection:
        result = connection.execute(text("select username from users"))
        for row in result:
            print("username:", row.username)


.. Above, the :meth:`_engine.Engine.connect` method returns a :class:`_engine.Connection` object, and by using it in a Python context manager (e.g. the ``with:`` statement) the :meth:`_engine.Connection.close` method is automatically invoked at the end of the block.  The :class:`_engine.Connection`, is a **proxy** object for an actual DBAPI connection. The DBAPI connection is retrieved from the connection pool at the point at which :class:`_engine.Connection` is created.

上の例では、 :meth:`_engine.Engine.connect` メソッドが :class:`_engine.Connection` オブジェクトを返し、それをPythonのコンテキストマネージャ(例えば ``with:`` 文)で使用することで、 :meth:`_engine.Connection.close` メソッドがブロックの最後で自動的に呼び出されます。 :class:`_engine.Connection` は、実際のDBAPI接続の **プロキシ** オブジェクトです。DBAPI接続は、 :class:`_engine.Connection` が作成された時点で接続プールから取得されます。

.. The object returned is known as :class:`_engine.CursorResult`, which references a DBAPI cursor and provides methods for fetching rows similar to that of the DBAPI cursor.   The DBAPI cursor will be closed by the :class:`_engine.CursorResult` when all of its result rows (if any) are exhausted.  A :class:`_engine.CursorResult` that returns no rows, such as that of an UPDATE statement (without any returned rows), releases cursor resources immediately upon construction.

返されるオブジェクトは :class:`_engine.CursorResult` として知られています。これはDBAPIカーソルを参照し、DBAPIカーソルと同様の行を取り出すためのメソッドを提供します。DBAPIカーソルは、その結果の行(もしあれば)がすべて使い果たされると、 :class:`_engine.CursorResult` によって閉じられます。UPDATE文のように(行が返されない)行を返さない :class:`_engine.CursorResult` は、構築されるとすぐにカーソルリソースを解放します。

.. When the :class:`_engine.Connection` is closed at the end of the ``with:`` block, the referenced DBAPI connection is :term:`released` to the connection pool.   From the perspective of the database itself, the connection pool will not actually "close" the connection assuming the pool has room to store this connection  for the next use.  When the connection is returned to the pool for re-use, the pooling mechanism issues a ``rollback()`` call on the DBAPI connection so that any transactional state or locks are removed (this is known as :ref:`pool_reset_on_return`), and the connection is ready for its next use.

:class:`_engine.Connection` が ``with:`` ブロックの最後で閉じられた場合、参照されたDBAPI接続は接続プールに対して :term:`released` されます。データベース自体の観点から見ると、接続プールに次の使用のためにこの接続を保存する余地があると仮定すると、接続プールは実際には接続を"close"しません。接続が再利用のためにプールに戻されると、プーリング機構はDBAPI接続に対して ``rollback()`` 呼び出しを発行して、トランザクション状態やロックが削除され(これは :ref:`pool_reset_on_return` として知られています)、接続が次に使用できるようになります。

.. Our example above illustrated the execution of a textual SQL string, which should be invoked by using the :func:`_expression.text` construct to indicate that we'd like to use textual SQL.  The :meth:`_engine.Connection.execute` method can of course accommodate more than that; see :ref:`tutorial_working_with_data` in the :ref:`unified_tutorial` for a tutorial.

上の例はテキストのSQL文字列の実行を示しています。これは :func:`_expression.text` 構文を使って呼び出され、テキストのSQLを使いたいことを示します。 :meth:`_engine.Connection.execute` メソッドはもちろんそれ以上のことにも対応できます。チュートリアルについては :ref:`unified_tutorial` の :ref:`tutorial_working_with_data` を参照してください。

Using Transactions
------------------

.. note::

  .. This section describes how to use transactions when working directly with :class:`_engine.Engine` and :class:`_engine.Connection` objects. When using the SQLAlchemy ORM, the public API for transaction control is via the :class:`.Session` object, which makes usage of the :class:`.Transaction` object internally. See :ref:`unitofwork_transaction` for further information.

  このセクションでは、 :class:`_engine.Engine` および :class:`_engine.Connection` オブジェクトを直接操作する場合にトランザクションを使用する方法について説明します。SQLAlchemy ORMを使用する場合、トランザクション制御のための公開APIは :class:`.Session` オブジェクトを経由します。これは :class:`.Transaction` オブジェクトを内部的に使用します。詳細は :ref:`unitofwork_transaction` を参照してください。

Commit As You Go
~~~~~~~~~~~~~~~~

.. The :class:`~sqlalchemy.engine.Connection` object always emits SQL statements within the context of a transaction block.   The first time the :meth:`_engine.Connection.execute` method is called to execute a SQL statement, this transaction is begun automatically, using a behavior known as **autobegin**.  The transaction remains in place for the scope of the :class:`_engine.Connection` object until the :meth:`_engine.Connection.commit` or :meth:`_engine.Connection.rollback` methods are called.  Subsequent to the transaction ending, the :class:`_engine.Connection` waits for the :meth:`_engine.Connection.execute` method to be called again, at which point it autobegins again.

:class:`~sqlalchemy.engine.Connection` オブジェクトは、常にトランザクションブロックのコンテキスト内でSQL文を発行します。SQL文を実行するために :meth:`_engine.Connection.execute` メソッドが最初に呼び出されると、このトランザクションは **autobegin** として知られる動作を使用して自動的に開始されます。トランザクションは、 :meth:`_engine.Connection.commit` または :meth:`_engine.Connection.rollback` メソッドが呼び出されるまで、 :class:`_engine.Connection` オブジェクトのスコープ内でそのまま残ります。トランザクションが終了した後、 :class:`_engine.Connection` は :meth:`_engine.Connection.execute` メソッドが再度呼び出されるのを待ち、呼び出された時点で再び自動開始します。

.. This calling style is known as **commit as you go**, and is illustrated in the example below::

この呼び出しスタイルは **commit as you go** と呼ばれ、以下の例で説明されています::

    with engine.connect() as connection:
        connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
        connection.execute(
            some_other_table.insert(), {"q": 8, "p": "this is some more data"}
        )

        connection.commit()  # commit the transaction

.. .. topic::
    .. the Python DBAPI is where autobegin actually happens The design of "commit as you go" is intended to be complementary to the design of the :term:`DBAPI`, which is the underlying database interface that SQLAlchemy interacts with. In the DBAPI, the ``connection`` object does not assume changes to the database will be automatically committed, instead requiring in the default case that the ``connection.commit()`` method is called in order to commit changes to the database. It should be noted that the DBAPI itself **does not have a begin() method at all**.  All Python DBAPIs implement "autobegin" as the primary means of managing transactions, and handle the job of emitting a statement like BEGIN on the connection when SQL statements are first emitted.  SQLAlchemy's API is basically re-stating this behavior in terms of higher level Python objects.

.. topic:: TL;DR;

    Python DBAPIはautobeginが実際に行われる場所です。"commit as you go"の設計は、SQLAlchemyが対話する基礎となるデータベースインタフェースである :term:`DBAPI` の設計を補完することを意図しています。DBAPIでは、``connection`` オブジェクトはデータベースへの変更が自動的にコミットされることを想定していません。代わりに、デフォルトのケースでは、データベースへの変更をコミットするために ``connection.commit()`` メソッドを呼び出す必要があります。DBAPI自体 **begin()メソッドをまったく持っていない** ことに注意してください。すべてのPython DBAPIは、トランザクションを管理する主要な手段として"autobegin"を実装し、SQL文が最初に発行されたときに接続上でBEGINのような文を発行するジョブを処理します。SQLAlchemyのAPIは基本的に、この動作をより高いレベルのPythonオブジェクトの観点から再記述しています。

.. In "commit as you go" style, we can call upon :meth:`_engine.Connection.commit` and :meth:`_engine.Connection.rollback` methods freely within an ongoing sequence of other statements emitted using :meth:`_engine.Connection.execute`; each time the transaction is ended, and a new statement is emitted, a new transaction begins implicitly::

"commit as you go"スタイルでは、 :meth:`_engine.Connection.commit` メソッドと :meth:`_engine.Connection.rollback` メソッドを、 :meth:`_engine.Connection.execute` を使用して発行された他の文の進行中のシーケンス内で自由に呼び出すことができます。トランザクションが終了して新しい文が発行されるたびに、新しいトランザクションが暗黙的に開始されます::

    with engine.connect() as connection:
        connection.execute(text("<some statement>"))
        connection.commit()  # commits "some statement"

        # new transaction starts
        connection.execute(text("<some other statement>"))
        connection.rollback()  # rolls back "some other statement"

        # new transaction starts
        connection.execute(text("<a third statement>"))
        connection.commit()  # commits "a third statement"

.. .. versionadded:: 2.0 "commit as you go" style is a new feature of SQLAlchemy 2.0.  It is also available in SQLAlchemy 1.4's "transitional" mode when using a "future" style engine.

.. versionadded:: 2.0の"commit as you go"スタイルは、SQLAlchemy 2.0の新機能です。"future"スタイルのエンジンを使用している場合は、SQLAlchemy 1.4の"transitional"モードでも使用できます。


Begin Once
~~~~~~~~~~

.. The :class:`_engine.Connection` object provides a more explicit transaction management style known as **begin once**. In contrast to "commit as you go", "begin once" allows the start point of the transaction to be stated explicitly, and allows that the transaction itself may be framed out as a context manager block so that the end of the transaction is instead implicit. To use "begin once", the :meth:`_engine.Connection.begin` method is used, which returns a :class:`.Transaction` object which represents the DBAPI transaction.  This object also supports explicit management via its own :meth:`_engine.Transaction.commit` and :meth:`_engine.Transaction.rollback` methods, but as a preferred practice also supports the context manager interface, where it will commit itself when the block ends normally and emit a rollback if an exception is raised, before propagating the exception outwards. Below illustrates the form of a "begin once" block::

:class:`_engine.Connection` オブジェクトは、 **begin once** として知られる、より明示的なトランザクション管理スタイルを提供します。"commit as you go"とは対照的に、"begin once"では、トランザクションの開始点を明示的に記述することができ、トランザクション自体をコンテキストマネージャブロックとしてフレームアウトして、トランザクションの終了を暗黙的にすることができます。"begin once"を使用するには、 :meth:`_engine.Connection.begin` メソッドを使用します。このメソッドは、DBAPIトランザクションを表す :class:`.Transaction` オブジェクトを返します。このオブジェクトは、独自の :meth:`_engine.Transaction.commit ` および :meth:`_engine.Transaction.rollback` メソッドによる明示的な管理もサポートしていますが、推奨される方法としては、コンテキストマネージャインターフェイスもサポートしています。コンテキストマネージャインターフェイスでは、ブロックが正常に終了したときに自分自身をコミットし、例外が発生した場合は例外を外部に伝播する前に行ルバックを発行します。以下に、"begin once"ブロックの形式を示します::

    with engine.connect() as connection:
        with connection.begin():
            connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
            connection.execute(
                some_other_table.insert(), {"q": 8, "p": "this is some more data"}
            )

        # transaction is committed

Connect and Begin Once from the Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. A convenient shorthand form for the above "begin once" block is to use the :meth:`_engine.Engine.begin` method at the level of the originating :class:`_engine.Engine` object, rather than performing the two separate steps of :meth:`_engine.Engine.connect` and :meth:`_engine.Connection.begin`; the :meth:`_engine.Engine.begin` method returns a special context manager that internally maintains both the context manager for the :class:`_engine.Connection` as well as the context manager for the :class:`_engine.Transaction` normally returned by the :meth:`_engine.Connection.begin` method::

上記の"begin once"ブロックの便利な省略形は、 :meth:`_engine.Engine.connect` と :meth:`_engine.Connection.begin` の2つの別々の手順を実行するのではなく、元の :class:`_engine.Engine` オブジェクトのレベルで :meth:`_engine.Engine.begin` メソッドを使用することです。 :meth:`_engine.Engine.begin` メソッドは、 :class:`_engine.Connection` のコンテキストマネージャと、通常 :meth:`_engine.Connection.begin` メソッドによって返される :class:`_engine.Transaction` のコンテキストマネージャの両方を内部で維持する特別なコンテキストマネージャを返します::

    with engine.begin() as connection:
        connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
        connection.execute(
            some_other_table.insert(), {"q": 8, "p": "this is some more data"}
        )

    # transaction is committed, and Connection is released to the connection
    # pool

.. tip::

    .. Within the :meth:`_engine.Engine.begin` block, we can call upon the :meth:`_engine.Connection.commit` or :meth:`_engine.Connection.rollback` methods, which will end the transaction normally demarcated by the block ahead of time.  However, if we do so, no further SQL operations may be emitted on the :class:`_engine.Connection` until the block ends::

    :meth:`_engine.Engine.begin` ブロック内では、 :meth:`_engine.Connection.commit` または :meth:`_engine.Connection.rollback` メソッドを呼び出すことができます。これらのメソッドは、通常はブロックによって事前に区切られているトランザクションを終了させます。しかし、これを行うと、ブロックが終了するまで、 :class:`_engine.Connection` に対してそれ以上のSQL操作が行われなくなります::

        >>> from sqlalchemy import create_engine
        >>> e = create_engine("sqlite://", echo=True)
        >>> with e.begin() as conn:
        ...     conn.commit()
        ...     conn.begin()
        2021-11-08 09:49:07,517 INFO sqlalchemy.engine.Engine BEGIN (implicit)
        2021-11-08 09:49:07,517 INFO sqlalchemy.engine.Engine COMMIT
        Traceback (most recent call last):
        ...
        sqlalchemy.exc.InvalidRequestError: Can't operate on closed transaction inside
        context manager.  Please complete the context manager before emitting
        further commands.

Mixing Styles
~~~~~~~~~~~~~

.. The "commit as you go" and "begin once" styles can be freely mixed within a single :meth:`_engine.Engine.connect` block, provided that the call to :meth:`_engine.Connection.begin` does not conflict with the "autobegin" behavior.  To accomplish this, :meth:`_engine.Connection.begin` should only be called either before any SQL statements have been emitted, or directly after a previous call to :meth:`_engine.Connection.commit` or :meth:`_engine.Connection.rollback`::

"commit as you go"スタイルと"begin once"スタイルは、 :meth:`_engine.Connection.begin` への呼び出しが"autobegin"の動作と競合しない限り、単一の :meth:`_engine.Engine.connect` ブロック内で自由に混在させることができます。これを実現するには、 :meth:`_engine.Connection.begin` は、SQL文が発行される前か、前回の :meth:`_engine.Connection.commit` または :meth:`_engine.Connection.rollback` の呼び出しの直後にのみ呼び出す必要があります::

    with engine.connect() as connection:
        with connection.begin():
            # run statements in a "begin once" block
            connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})

        # transaction is committed

        # run a new statement outside of a block. The connection
        # autobegins
        connection.execute(
            some_other_table.insert(), {"q": 8, "p": "this is some more data"}
        )

        # commit explicitly
        connection.commit()

        # can use a "begin once" block here
        with connection.begin():
            # run more statements
            connection.execute(...)

.. When developing code that uses "begin once", the library will raise :class:`_exc.InvalidRequestError` if a transaction was already "autobegun".

"begin once"を使用するコードを開発する場合、ライブラリはトランザクションが既に"autobegun"されていれば :class:`_exc.InvalidRequestError` を発生させます。

.. _dbapi_autocommit:

Setting Transaction Isolation Levels including DBAPI Autocommit
---------------------------------------------------------------

.. Most DBAPIs support the concept of configurable transaction :term:`isolation` levels.  These are traditionally the four levels "READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ" and "SERIALIZABLE".  These are usually applied to a DBAPI connection before it begins a new transaction, noting that most DBAPIs will begin this transaction implicitly when SQL statements are first emitted.

ほとんどのDBAPIは、設定可能なトランザクション :term:`isolation` レベルの概念をサポートしています。これらは伝統的に"READ UNCOMMITTED"、"READ COMMITTED"、"REPEATABLE READ"、"SERIALIZABLE"の4つのレベルです。これらは通常、新しいトランザクションを開始する前にDBAPI接続に適用されますが、ほとんどのDBAPIはSQL文が最初に発行されたときに暗黙的にこのトランザクションを開始することに注意してください。

.. DBAPIs that support isolation levels also usually support the concept of true "autocommit", which means that the DBAPI connection itself will be placed into a non-transactional autocommit mode. This usually means that the typical DBAPI behavior of emitting "BEGIN" to the database automatically no longer occurs, but it may also include other directives. SQLAlchemy treats the concept of "autocommit" like any other isolation level; in that it is an isolation level that loses not only "read committed" but also loses atomicity.

独立性レベルをサポートするDBAPIは、通常、真の"autocommit"の概念もサポートします。これは、DBAPI接続自体が非トランザクション・オートコミット・モードになることを意味します。これは通常、データベースに"BEGIN"を自動的に発行するという一般的なDBAPIの動作が発生しなくなることを意味しますが、他のディレクティブが含まれる場合もあります。SQLAlchemyでは、"autocommit"の概念を他の独立性レベルと同様に扱います。つまり、"autocommit"は"read commited"だけでなく、原子性も失う独立性レベルです。

.. tip::

    .. It is important to note, as will be discussed further in the section below at :ref:`dbapi_autocommit_understanding`, that "autocommit" isolation level like any other isolation level does **not** affect the "transactional" behavior of the :class:`_engine.Connection` object, which continues to call upon DBAPI ``.commit()`` and ``.rollback()`` methods (they just have no effect under autocommit), and for which the ``.begin()`` method assumes the DBAPI will start a transaction implicitly (which means that SQLAlchemy's "begin" **does not change autocommit mode**).

    以下のセクションの :ref:`dbapi_autocommit_understanding` で詳しく説明しますが、"autocommit"独立性レベルは、他の独立性レベルと同様に、 :class:`_engine.Connection` オブジェクトの"transactional"動作に **影響しない** ことに注意してください。このオブジェクトは、DBAPIの ``.commit()``` メソッドと ``.rollback()`` メソッドを呼び出し続けます(これらはオートコミットでは効果がありません)。また、 ``.begin()`` メソッドは、DBAPIが暗黙的にトランザクションを開始することを想定しています(つまり、SQLAlchemyの"begin" **はオートコミットモードを変更しません** )。

.. SQLAlchemy dialects should support these isolation levels as well as autocommit to as great a degree as possible.

SQLAlchemyダイアレクトでは、これらの独立性レベルをサポートするとともに、可能な限り大きなオートコミットをサポートする必要があります。

Setting Isolation Level or DBAPI Autocommit for a Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. For an individual :class:`_engine.Connection` object that's acquired from :meth:`.Engine.connect`, the isolation level can be set for the duration of that :class:`_engine.Connection` object using the :meth:`_engine.Connection.execution_options` method. The parameter is known as :paramref:`_engine.Connection.execution_options.isolation_level` and the values are strings which are typically a subset of the following names::

:meth:`.Engine.connect` から取得した個々の :class:`_engine.Connection` オブジェクトに対して、 :meth:`_engine.Connection.execution_options` メソッドを使用して、その :class:`_engine.Connection` オブジェクトの期間に対して独立性レベルを設定することができます。パラメータは :paramref:`_engine.Connection.execution_options.isolation_level` として知られており、値は文字列で、通常は次の名前のサブセットです::

    # possible values for Connection.execution_options(isolation_level="<value>")

    "AUTOCOMMIT"
    "READ COMMITTED"
    "READ UNCOMMITTED"
    "REPEATABLE READ"
    "SERIALIZABLE"

.. Not every DBAPI supports every value; if an unsupported value is used for a certain backend, an error is raised.

すべてのDBAPIがすべての値をサポートしているわけではありません。サポートされていない値が特定のバックエンドで使用されると、エラーが発生します。

.. For example, to force REPEATABLE READ on a specific connection, then begin a transaction::

たとえば、特定の接続でREPEATABLE READを強制するには、次のようにトランザクションを開始します::

    with engine.connect().execution_options(
        isolation_level="REPEATABLE READ"
    ) as connection:
        with connection.begin():
            connection.execute(text("<statement>"))

.. .. tip::
    .. The return value of the :meth:`_engine.Connection.execution_options` method is the same :class:`_engine.Connection` object upon which the method was called, meaning, it modifies the state of the :class:`_engine.Connection` object in place.  This is a new behavior as of SQLAlchemy 2.0.  This behavior does not apply to the :meth:`_engine.Engine.execution_options` method; that method still returns a copy of the :class:`.Engine` and as described below may be used to construct multiple :class:`.Engine` objects with different execution options, which nonetheless share the same dialect and connection pool.

.. tip::
    :meth:`_engine.Connection.execution_options` メソッドの戻り値は、このメソッドが呼び出された :class:`_engine.Connection` オブジェクトと同じです。つまり、 :class:`_engine.Connection` オブジェクトの状態を適切に変更します。これはSQLAlchemy 2.0の新しい動作です。この動作は :meth:`_engine.Engine.execution_options` メソッドには適用されません。このメソッドは :class:`.Engine` のコピーを返します。また、以下に説明するように、実行オプションが異なる複数の :class:`.Engine` オブジェクトを構築するために使用できますが、これらのオブジェクトは同じダイアレクトと接続プールを共有します。

.. note::
    .. The :paramref:`_engine.Connection.execution_options.isolation_level` parameter necessarily does not apply to statement level options, such as that of :meth:`_sql.Executable.execution_options`, and will be rejected if set at this level. This because the option must be set on a DBAPI connection on a per-transaction basis.

    :paramref:`_engine.Connection.execution_options.isolation_level` パラメータは、:meth:`_sql.Executable.execution_options` のような文レベルのオプションには適用されず、このレベルで設定された場合は拒否されます。これは、このオプションはトランザクションごとにDBAPI接続で設定する必要があるためです。

Setting Isolation Level or DBAPI Autocommit for an Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The :paramref:`_engine.Connection.execution_options.isolation_level` option may also be set engine wide, as is often preferable.  This may be achieved by passing the :paramref:`_sa.create_engine.isolation_level` parameter to :func:`.sa.create_engine`::

:paramref:`_engine.Connection.execution_options.isolation_level` オプションは、よくあるようにエンジン全体に設定することもできます。これは、 :paramref:`_sa.create_engine.isolation_level` パラメータを :func:`.sa.create_engine` に渡すことで実現できます::

    from sqlalchemy import create_engine

    eng = create_engine(
        "postgresql://scott:tiger@localhost/test", isolation_level="REPEATABLE READ"
    )

.. With the above setting, each new DBAPI connection the moment it's created will be set to use a ``"REPEATABLE READ"`` isolation level setting for all subsequent operations.

上記の設定では、新しいDBAPI接続が作成された時点で、以降のすべての操作に対して ``"REPEATABLE READ"`` の独立性レベルが設定されます。

.. _dbapi_autocommit_multiple:

Maintaining Multiple Isolation Levels for a Single Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The isolation level may also be set per engine, with a potentially greater level of flexibility, using either the :paramref:`_sa.create_engine.execution_options` parameter to :func:`_sa.create_engine` or the :meth:`_engine.Engine.execution_options` method, the latter of which will create a copy of the :class:`.Engine` that shares the dialect and connection pool of the original engine, but has its own per-connection isolation level setting::

独立性レベルは、 :func:`_sa.create_engine` の :paramref:`_sa.create_engine.execution_options` パラメータか、 :meth:`_engine.Engine.execution_options` メソッドのどちらかを使用して、エンジンごとに設定することもできます。後者は、元のエンジンのダイアレクトと接続プールを共有する :class:`.Engine` のコピーを作成しますが、接続ごとに独自の独立性レベル設定があります::

    from sqlalchemy import create_engine

    eng = create_engine(
        "postgresql+psycopg2://scott:tiger@localhost/test",
        execution_options={"isolation_level": "REPEATABLE READ"},
    )

.. With the above setting, the DBAPI connection will be set to use a ``"REPEATABLE READ"`` isolation level setting for each new transaction begun; but the connection as pooled will be reset to the original isolation level that was present when the connection first occurred.   At the level of :func:`_sa.create_engine`, the end effect is not any different from using the :paramref:`_sa.create_engine.isolation_level` parameter.

上記の設定では、DBAPI接続は、開始された新しいトランザクションごとに ``"REPEATABLE READ"`` の独立性レベル設定を使用するように設定されますが、プールされた接続は、接続が最初に発生したときに存在していた元の独立性レベルにリセットされます。 :func:`_sa.create_engine` のレベルでは、終了効果は :paramref:`_sa.create_engine.isolation_level` パラメータを使用した場合と何も変わりません。

.. However, an application that frequently chooses to run operations within different isolation levels may wish to create multiple "sub-engines" of a lead :class:`_engine.Engine`, each of which will be configured to a different isolation level. One such use case is an application that has operations that break into "transactional" and "read-only" operations, a separate :class:`_engine.Engine` that makes use of ``"AUTOCOMMIT"`` may be separated off from the main engine::

しかし、異なる独立性レベル内で操作を実行することを頻繁に選択するアプリケーションは、それぞれが異なる独立性レベルに設定される、リード :class:`_engine.Engine` の複数の"sub-engines"を作成したい場合があります。そのようなユースケースの1つは、"トランザクション"操作と"読み取り専用"操作に分割される操作を持つアプリケーションで、 ``"AUTOCOMMIT"`` を使用する別の :class:`_engine.Engine` をメインエンジンから分離することができます::

    from sqlalchemy import create_engine

    eng = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")

    autocommit_engine = eng.execution_options(isolation_level="AUTOCOMMIT")

.. Above, the :meth:`_engine.Engine.execution_options` method creates a shallow copy of the original :class:`_engine.Engine`.  Both ``eng`` and ``autocommit_engine`` share the same dialect and connection pool.  However, the "AUTOCOMMIT" mode will be set upon connections when they are acquired from the ``autocommit_engine``.

上の例では、 :meth:`_engine.Engine.execution_options` メソッドが元の :class:`_engine.Engine` のシャ行コピーを作成します。 ``eng`` と ``autocommit_engine`` は同じダイアレクトと接続プールを共有します。しかし、 ``autocommit_engine`` から取得された接続には"AUTOCOMMIT"モードが設定されます。

.. The isolation level setting, regardless of which one it is, is unconditionally reverted when a connection is returned to the connection pool.

独立性レベルの設定は、どの設定であっても、接続が接続プールに戻されると無条件に元に戻されます。

.. seealso::

      :ref:`SQLite Transaction Isolation <sqlite_isolation_level>`

      :ref:`PostgreSQL Transaction Isolation <postgresql_isolation_level>`

      :ref:`MySQL Transaction Isolation <mysql_isolation_level>`

      :ref:`SQL Server Transaction Isolation <mssql_isolation_level>`

      :ref:`Oracle Transaction Isolation <oracle_isolation_level>`

      :ref:`session_transaction_isolation` - for the ORM

      .. :ref:`faq_execute_retry_autocommit` - a recipe that uses DBAPI autocommit to transparently reconnect to the database for read-only operations

      :ref:`faq_execute_retry_autocommit` - DBAPIオートコミットを使用して、読み込み専用操作のためにデータベースに透過的に再接続するレシピ

.. _dbapi_autocommit_understanding:

Understanding the DBAPI-Level Autocommit Isolation Level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. In the parent section, we introduced the concept of the :paramref:`_engine.Connection.execution_options.isolation_level` parameter and how it can be used to set database isolation levels, including DBAPI-level "autocommit" which is treated by SQLAlchemy as another transaction isolation level. In this section we will attempt to clarify the implications of this approach.

親のセクションでは、 :paramref:`_engine.Connection.execution_options.isolation_level` パラメータの概念と、それを使用してデータベースの独立性レベルを設定する方法を紹介しました。これには、SQLAlchemyによって別のトランザクション独立性レベルとして扱われるDB APIレベルの"autocommit"も含まれます。このセクションでは、このアプ行チの意味を明確にすることを試みます。

.. If we wanted to check out a :class:`_engine.Connection` object and use it "autocommit" mode, we would proceed as follows::

:class:`_engine.Connection` オブジェクトをチェックアウトして"autocommit"モードを使いたい場合は、次のようにします::

    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        connection.execute(text("<statement>"))
        connection.execute(text("<statement>"))

.. Above illustrates normal usage of "DBAPI autocommit" mode.   There is no need to make use of methods such as :meth:`_engine.Connection.begin` or :meth:`_engine.Connection.commit`, as all statements are committed to the database immediately.  When the block ends, the :class:`_engine.Connection` object will revert the "autocommit" isolation level, and the DBAPI connection is released to the connection pool where the DBAPI ``connection.rollback()`` method will normally be invoked, but as the above statements were already committed, this rollback has no change on the state of the database.

上の図は、"DBAPI autocommit"モードの通常の使用法を示しています。 :meth:`_engine.Connection.begin` や :meth:`_engine.Connection.commit` のようなメソッドを使う必要はありません。全ての文は即座にデータベースにコミットされます。ブロックが終了すると、 :class:`_engine.Connection` オブジェクトは"autocommit"独立性レベルを元に戻し、DBAPI接続はコネクションプールに解放されます。そこではDBAPIの ``connection.rollback()`` メソッドが通常呼び出されますが、上の文は既にコミットされているので、この行ルバックはデータベースの状態を変更しません。

.. It is important to note that "autocommit" mode persists even when the :meth:`_engine.Connection.begin` method is called; the DBAPI will not emit any BEGIN to the database, nor will it emit COMMIT when :meth:`_engine.Connection.commit` is called.  This usage is also not an error scenario, as it is expected that the "autocommit" isolation level may be applied to code that otherwise was written assuming a transactional context; the "isolation level" is, after all, a configurational detail of the transaction itself just like any other isolation level.

"autocommit"モードは :meth:`_engine.Connection.begin` メソッドが呼び出されても持続することに注意してください。DBAPIはデータベースに対してBEGINを発行しませんし、 :meth:`_engine.Connection.commit` が呼び出されてもCOMMITを発行しません。"autocommit"独立性レベルは、トランザクションコンテキストを想定して作成されたコードに適用されることが想定されているため、この使用方法もエラーシナリオではありません。"独立性レベル"は、他の独立性レベルと同様に、トランザクション自体の設定の詳細です。

.. In the example below, statements remain **autocommitting** regardless of SQLAlchemy-level transaction blocks::

次の例では、SQLAlchemyレベルのトランザクションブロックに関係なく、文は **autocommitting** のままです::

    with engine.connect() as connection:
        connection = connection.execution_options(isolation_level="AUTOCOMMIT")

        # this begin() does not affect the DBAPI connection, isolation stays at AUTOCOMMIT
        with connection.begin() as trans:
            connection.execute(text("<statement>"))
            connection.execute(text("<statement>"))

.. When we run a block like the above with logging turned on, the logging will attempt to indicate that while a DBAPI level ``.commit()`` is called, it probably will have no effect due to autocommit mode:

ロギングを有効にして上記のようなブロックを実行すると、ロギングはDBAPIレベルの ``.commit()`` が呼び出されている間、オートコミットモードのためにおそらく何の効果もないことを示そうとします。

.. sourcecode:: text

    INFO sqlalchemy.engine.Engine BEGIN (implicit)
    ...
    INFO sqlalchemy.engine.Engine COMMIT using DBAPI connection.commit(), DBAPI should ignore due to autocommit mode

.. At the same time, even though we are using "DBAPI autocommit", SQLAlchemy's transactional semantics, that is, the in-Python behavior of :meth:`_engine.Connection.begin` as well as the behavior of "autobegin", **remain in place, even though these don't impact the DBAPI connection itself**.  To illustrate, the code below will raise an error, as :meth:`_engine.Connection.begin` is being called after autobegin has already occurred::

同時に、SQLAlchemyのトランザクションセマンティクスである"DBAPI autocommit"、つまり :meth:`_engine.Connection.begin` のPython内での振る舞いや "autobegin" の振る舞いを使用しても、 **DBAPI接続自体には影響しませんが、そのまま残ります** 。たとえば、以下のコードでは、autobeginがすでに発生した後に :meth:`_engine.Connection.begin` が呼び出されるため、エラーが発生します::

    with engine.connect() as connection:
        connection = connection.execution_options(isolation_level="AUTOCOMMIT")

        # "transaction" is autobegin (but has no effect due to autocommit)
        connection.execute(text("<statement>"))

        # this will raise; "transaction" is already begun
        with connection.begin() as trans:
            connection.execute(text("<statement>"))

.. The above example also demonstrates the same theme that the "autocommit" isolation level is a configurational detail of the underlying database transaction, and is independent of the begin/commit behavior of the SQLAlchemy Connection object. The "autocommit" mode will not interact with :meth:`_engine.Connection.begin` in any way and the :class:`_engine.Connection` does not consult this status when performing its own state changes with regards to the transaction (with the exception of suggesting within engine logging that these blocks are not actually committing). The rationale for this design is to maintain a completely consistent usage pattern with the :class:`_engine.Connection` where DBAPI-autocommit mode can be changed independently without indicating any code changes elsewhere.

上記の例では、"autocommit"分離レベルが基礎となるデータベース・トランザクションの構成の詳細であり、SQLAlchemy Connectionオブジェクトの開始/コミット動作とは無関係であるという同じテーマについても説明しています。"autocommit"モードは :meth:`_engine.Connection.begin` とは一切相互作用せず、 :class:`_engine.Connection` はトランザクションに関して自身の状態を変更する際にこの状態を参照しません(ただし、エンジン・ロギング内では、これらのブロックが実際にコミットされていないことが示唆されます)。この設計の理論的根拠は、 :class:`_engine.Connection` と完全に一貫した使用パターンを維持することにあります。ここで、DBAPI-autocommitモードは、他の場所でコードの変更を示すことなく、独立して変更できます。

Changing Between Isolation Levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. .. topic::

    .. TL;DR; prefer to use individual :class:`_engine.Connection` objects each with just one isolation level, rather than switching isolation on a single :class:`_engine.Connection`.  The code will be easier to read and less error prone.

.. topic:: TL;DR;

    単一の :class:`_engine.Connection` で独立性を切り替えるのではなく、それぞれが1つの独立性レベルを持つ個々の :class:`_engine.Connection` オブジェクトを使用することを好みます。コードが読みやすくなり、エラーが発生しにくくなります。

.. Isolation level settings, including autocommit mode, are reset automatically when the connection is released back to the connection pool. Therefore it is preferable to avoid trying to switch isolation levels on a single :class:`_engine.Connection` object as this leads to excess verbosity.

オートコミット・モードを含む独立性レベルの設定は、接続が解放されて接続プールに戻されたときに自動的にリセットされます。したがって、単一の :class:`_engine.Connection` オブジェクトで独立性レベルを切り替えようとすることは、過剰な冗長性につながるため、避けることをお勧めします。

.. To illustrate how to use "autocommit" in an ad-hoc mode within the scope of a single :class:`_engine.Connection` checkout, the :paramref:`_engine.Connection.execution_options.isolation_level` parameter must be re-applied with the previous isolation level.  The previous section illustrated an attempt to call :meth:`_engine.Connection.begin` in order to start a transaction while autocommit was taking place; we can rewrite that example to actually do so by first reverting the isolation level before we call upon :meth:`_engine.Connection.begin`::

単一の :class:`_engine.Connection` チェックアウトの範囲内でアドホックモードで"autocommit"を使用する方法を説明するには、 :paramref:`_engine.Connection.execution_options.isolation_level` パラメータを以前の独立性レベルで再適用する必要があります。前のセクションでは、オートコミットが行われている間にトランザクションを開始するために :meth:`_engine.Connection.begin` を呼び出そうとする試みを説明しました。 :meth:`_engine.Connection.begin` を呼び出す前に、まず独立性レベルを元に戻すことで、実際にそうするように例を書き直すことができます::

    # if we wanted to flip autocommit on and off on a single connection/
    # which... we usually don't.

    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")

        # run statement(s) in autocommit mode
        connection.execute(text("<statement>"))

        # "commit" the autobegun "transaction"
        connection.commit()

        # switch to default isolation level
        connection.execution_options(isolation_level=connection.default_isolation_level)

        # use a begin block
        with connection.begin() as trans:
            connection.execute(text("<statement>"))

.. Above, to manually revert the isolation level we made use of :attr:`_engine.Connection.default_isolation_level` to restore the default isolation level (assuming that's what we want here). However, it's probably a better idea to work with the architecture of of the :class:`_engine.Connection` which already handles resetting of isolation level automatically upon checkin. The **preferred** way to write the above is to use two blocks ::

上記では、独立性レベルを手動で元に戻すために、 :attr:`_engine.Connection.default_isolation_level` を使用してデフォルトの独立性レベルを復元しました(ここではそれが必要であると仮定しています)。しかし、チェックイン時に自動的に独立性レベルのリセットを処理する :class:`_engine.Connection` のアーキテクチャで作業する方がおそらく良い考えでしょう。上記の **推奨** 方法は、2つのブロックを使用することです::

    # use an autocommit block
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        # run statement in autocommit mode
        connection.execute(text("<statement>"))

    # use a regular block
    with engine.begin() as connection:
        connection.execute(text("<statement>"))

.. To sum up:

まとめると:

.. 1. "DBAPI level autocommit" isolation level is entirely independent of the :class:`_engine.Connection` object's notion of "begin" and "commit"

.. 2. use individual :class:`_engine.Connection` checkouts per isolation level. Avoid trying to change back and forth between "autocommit" on a single connection checkout; let the engine do the work of restoring default isolation levels

1. "DBAPI level autocommit"独立性レベルは、:class:`_engine.Connection` オブジェクトの"begin"と"commit"の概念から完全に独立しています。

2. 独立性レベルごとに個別の :class:`_engine.Connection` チェックアウトを使用します。1回の接続チェックアウトで「自動コミット」の間を行ったり来たりすることは避けてください。デフォルトの独立性レベルを復元する作業はエンジンに任せてください。

.. _engine_stream_results:

Using Server Side Cursors (a.k.a. stream results)
-------------------------------------------------

.. Some backends feature explicit support for the concept of "server side cursors" versus "client side cursors".  A client side cursor here means that the database driver fully fetches all rows from a result set into memory before returning from a statement execution.  Drivers such as those of PostgreSQL and MySQL/MariaDB generally use client side cursors by default.   A server side cursor, by contrast, indicates that result rows remain pending within the database server's state as result rows are consumed by the client.  The drivers for Oracle generally use a "server side" model, for example, and the SQLite dialect, while not using a real "client / server" architecture, still uses an unbuffered result fetching approach that will leave result rows outside of process memory before they are consumed.

一部のバックエンドでは、"サーバー側カーソル"と"クライアント側カーソル"の概念が明示的にサポートされています。ここでいうクライアント側カーソルとは、データベース・ドライバが文の実行から戻る前に、結果セットからすべての行を完全にメモリにフェッチすることを意味します。PostgreSQLやMySQL/MariaDBなどのドライバでは、通常、デフォルトでクライアント側カーソルが使用されます。これとは対照的に、サーバー側カーソルは、結果行がクライアントによってコンシュームされるときに、結果行がデータベース・サーバの状態内で保留中のままであることを示します。Oracleのドライバでは、通常、たとえば"サーバー側"モデルが使用されます。SQLiteダイアレクトでは、実際の"クライアント/サーバ"アーキテクチャは使用されませんが、結果行が消費される前にプロセス・メモリの外部に残すバッファなしの結果フェッチ・アプ行チが使用されます。

.. .. topic:: What we really mean is "buffered" vs. "unbuffered" results Server side cursors also imply a wider set of features with relational databases, such as the ability to "scroll" a cursor forwards and backwards.  SQLAlchemy does not include any explicit support for these behaviors; within SQLAlchemy itself, the general term "server side cursors" should be considered to mean "unbuffered results" and "client side cursors" means "result rows are buffered into memory before the first row is returned".   To work with a richer "server side cursor" featureset specific to a certain DBAPI driver, see the section :ref:`dbapi_connections_cursor`.

.. topic:: TL;DR;

    "バッファされた"結果と"バッファされていない"結果の本当の意味は、サーバ側カーソルは、カーソルを前後に"スク行ル"する機能など、リレーショナルデータベースのより広範な機能も意味します。SQLAlchemy自体には、これらの動作に対する明示的なサポートは含まれていません。SQLAlchemy自体の中では、一般的な用語"サーバ側カーソル"は"バッファされていない結果"を意味し、"クライアント側カーソル"は"最初の行が返される前に結果の行がメモリにバッファされる"ことを意味します。特定のDBAPIドライバに固有のより豊富な"サーバ側カーソル"機能セットを使用するには、 :ref:`dbapi_connections_cursor` を参照してください。

.. From this basic architecture it follows that a "server side cursor" is more memory efficient when fetching very large result sets, while at the same time may introduce more complexity in the client/server communication process and be less efficient for small result sets (typically less than 10000 rows).

この基本的なアーキテクチャから、"サーバ側カーソル"は、非常に大きな結果セットをフェッチする場合にメモリ効率が高くなりますが、同時に、クライアント/サーバ通信プロセスがより複雑になり、小さな結果セット(通常は10000行未満)の場合には効率が低くなる可能性があります。

.. For those dialects that have conditional support for buffered or unbuffered results, there are usually caveats to the use of the "unbuffered", or server side cursor mode.   When using the psycopg2 dialect for example, an error is raised if a server side cursor is used with any kind of DML or DDL statement.  When using MySQL drivers with a server side cursor, the DBAPI connection is in a more fragile state and does not recover as gracefully from error conditions nor will it allow a rollback to proceed until the cursor is fully closed.

バッファリングされた結果またはバッファリングされていない結果を条件付きでサポートするダイアレクトでは、通常、"バッファリングされていない"、つまりサーバー側カーソル・モードの使用に注意が必要です。たとえば、psycopg2ダイアレクトを使用する場合、サーバー側カーソルが任意の種類のDMLまたはDDL文とともに使用されると、エラーが発生します。サーバー側カーソルでMySQLドライバを使用すると、DBAPI接続はより脆弱な状態になり、エラー状態から正常に回復せず、カーソルが完全に閉じるまで行ルバックを続行できません。

.. For this reason, SQLAlchemy's dialects will always default to the less error prone version of a cursor, which means for PostgreSQL and MySQL dialects it defaults to a buffered, "client side" cursor where the full set of results is pulled into memory before any fetch methods are called from the cursor.  This mode of operation is appropriate in the **vast majority** of cases; unbuffered cursors are not generally useful except in the uncommon case of an application fetching a very large number of rows in chunks, where the processing of these rows can be complete before more rows are fetched.

このため、SQLAlchemyのダイアレクトでは、常にデフォルトでエラーが発生しにくいバージョンのカーソルが使用されます。つまり、PostgreSQLおよびMySQLのダイアレクトでは、デフォルトでバッファされた"クライアント側"のカーソルが使用され、カーソルからフェッチメソッドが呼び出される前に、結果の完全なセットがメモリにプルされます。この操作モードは、 **大多数** の場合に適しています。バッファされていないカーソルは、一般的には有用ではありません。ただし、アプリケーションがチャンク内の非常に多数の行をフェッチするというまれなケースでは、これらの行の処理が、さらに行がフェッチされる前に完了する可能性があります。

.. For database drivers that provide client and server side cursor options, the :paramref:`_engine.Connection.execution_options.stream_results` and :paramref:`_engine.Connection.execution_options.yield_per` execution options provide access to "server side cursors" on a per-:class:`_engine.Connection` or per-statement basis.    Similar options exist when using an ORM :class:`_orm.Session` as well.

クライアント側およびサーバー側のカーソルオプションを提供するデータベースドライバの場合、 :paramref:`_engine.Connection.execution_options.stream_results` および :paramref:`_engine.Connection.execution_options.yield_per` 実行オプションは、 :class:`_engine.Connection` ごとまたはステートメントごとに"サーバー側カーソル"へのアクセスを提供します。同様のオプションは、ORM :class:`_orm.Session` を使用する場合にも存在します。

Streaming with a fixed buffer via yield_per
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. As individual row-fetch operations with fully unbuffered server side cursors are typically more expensive than fetching batches of rows at once, The :paramref:`_engine.Connection.execution_options.yield_per` execution option configures a :class:`_engine.Connection` or statement to make use of server-side cursors as are available, while at the same time configuring a fixed-size buffer of rows that will retrieve rows from the server in batches as they are consumed. This parameter may be to a positive integer value using the :meth:`_engine.Connection.execution_options` method on :class:`_engine.Connection` or on a statement using the :meth:`.Executable.execution_options` method.

完全にバッファリングされていないサーバ側カーソルを使用した個々の行フェッチ操作は、通常、一度に行のバッチをフェッチするよりもコストがかかるため、 :paramref:`_engine.Connection.execution_options.yield_per` 実行オプションは、 :class:`_engine.Connection` またはステートメントが利用可能なサーバ側カーソルを使用するように設定し、同時に、消費された行をバッチでサーバから取得する行の固定サイズのバッファを設定します。このパラメータは、 :class:`_engine.Connection` の :meth:`_engine.Connection.execution_options` メソッド、または :meth:`.Executable.execution_options` メソッドを使用したステートメントで、正の整数値にすることができます。

.. .. versionadded:: 1.4.40 :paramref:`_engine.Connection.execution_options.yield_per` as a Core-only option is new as of SQLAlchemy 1.4.40; for prior 1.4 versions, use :paramref:`_engine.Connection.execution_options.stream_results` directly in combination with :meth:`_engine.Result.yield_per`.

.. versionadded:: 1.4.40 :paramref:`_engine.Connection.execution_options.yield_per` がコアのみのオプションとして追加されました。これはSQLAlchemy 1.4.40で新しくなりました。1.4より前のバージョンでは、 :paramref:`_engine.Connection.execution_options.stream_results` を :meth:`_engine.Result.yield_per` と直接組み合わせて使用してください。

.. Using this option is equivalent to manually setting the :paramref:`_engine.Connection.execution_options.stream_results` option, described in the next section, and then invoking the :meth:`_engine.Result.yield_per` method on the :class:`_engine.Result` object with the given integer value.   In both cases, the effect this combination has includes:

このオプションを使用することは、次のセクションで説明する :paramref:`_engine.Connection.execution_options.stream_results` オプションを手動で設定し、指定された整数値を使用して :class:`_engine.Result` オブジェクトで :meth:`_engine.Result.yield_per` メソッドを呼び出すことと同じです。どちらの場合も、この組み合わせには次のような効果があります。

.. * server side cursors mode is selected for the given backend, if available and not already the default behavior for that backend
.. * as result rows are fetched, they will be buffered in batches, where the size of each batch up until the last batch will be equal to the integer argument passed to the :paramref:`_engine.Connection.execution_options.yield_per` option or the :meth:`_engine.Result.yield_per` method; the last batch is then sized against the remaining rows fewer than this size
.. * The default partition size used by the :meth:`_engine.Result.partitions` method, if used, will be made equal to this integer size as well.

* 指定されたバックエンドでサーバサイドカーソルモードが選択されている(利用可能で、そのバックエンドのデフォルトの動作になっていない場合)
* 結果の行が取り出されると、それらはバッチ単位でバッファリングされます。ここで、最後のバッチまでの各バッチのサイズは、 :paramref:`_engine.Connection.execution_options.yield_per` オプションまたは :meth:`_engine.Result.yield_per` メソッドに渡された整数引数と等しくなります。最後のバッチは、このサイズより小さい残りの行に対してサイズ設定されます。
*  :meth:`_engine.Result.partitions` メソッドで使用されるデフォルトのパーティションサイズも、この整数サイズと等しくなります。

.. These three behaviors are illustrated in the example below::

これらの3つの動作を次の例に示します::

    with engine.connect() as conn:
        with conn.execution_options(yield_per=100).execute(
            text("select * from table")
        ) as result:
            for partition in result.partitions():
                # partition is an iterable that will be at most 100 items
                for row in partition:
                    print(f"{row}")

.. The above example illustrates the combination of ``yield_per=100`` along with using the :meth:`_engine.Result.partitions` method to run processing on rows in batches that match the size fetched from the server.   The use of :meth:`_engine.Result.partitions` is optional, and if the :class:`_engine.Result` is iterated directly, a new batch of rows will be buffered for each 100 rows fetched.    Calling a method such as :meth:`_engine.Result.all` should **not** be used, as this will fully fetch all remaining rows at once and defeat the purpose of using ``yield_per``.

上の例では 、:meth:`_engine.Result.partitions` メソッドを使用して、サーバから取得したサイズに一致するバッチの行に対して処理を実行することと、 ``yield_per=100`` という組み合わせを示しています。 :meth:`_engine.Result.partitions` の使用はオプションであり、 :class:`_engine.Result` が直接反復される場合、取得された100行ごとに新しいバッチの行がバッファされます。 :meth:`_engine.Result.all` のようなメソッドを呼び出すことは **しないでください** 。なぜなら、これは残りのすべての行を一度に完全に取得し、 ``yield_per`` を使用する目的を損なうからです。

.. tip::

    .. The :class:`.Result` object may be used as a context manager as illustrated above.  When iterating with a server-side cursor, this is the best way to ensure the :class:`.Result` object is closed, even if exceptions are raised within the iteration process.

    :class:`.Result` オブジェクトは、上で説明したように、コンテキストマネージャとして使用することができます。サーバ側のカーソルで反復する場合、これは、反復プロセス内で例外が発生した場合でも、 :class:`.Result` オブジェクトが閉じられるようにする最善の方法です。

.. The :paramref:`_engine.Connection.execution_options.yield_per` option is portable to the ORM as well, used by a :class:`_orm.Session` to fetch ORM objects, where it also limits the amount of ORM objects generated at once.  See the section :ref:`orm_queryguide_yield_per` - in the :ref:`queryguide_toplevel` for further background on using :paramref:`_engine.Connection.execution_options.yield_per` with the ORM.

:paramref:`_engine.Connection.execution_options.yield_per` オプションはORMにも移植できます。これは :class:`_orm.Session` がORMオブジェクトを取得するために使用し、一度に生成されるORMオブジェクトの量も制限します。ORMで :paramref:`_engine.Connection.execution_options.yield_per` を使用する背景については、 :ref:`queryguide_toplevel` の :ref:`orm_queryguide_yield_per` 節を参照してください。

.. .. versionadded:: 1.4.40 Added :paramref:`_engine.Connection.execution_options.yield_per` as a Core level execution option to conveniently set streaming results, buffer size, and partition size all at once in a manner that is transferrable to that of the ORM's similar use case.

.. versionadded:: 1.4.40 Coreレベルの実行オプションとして :paramref:`_engine.Connection.execution_options.yield_per` が追加されました。これにより、ストリーミング結果、バッファサイズ、およびパーティションサイズを、ORMの同様のユースケースに転送可能な方法で一度に設定できます。

.. _engine_stream_results_sr:

Streaming with a dynamically growing buffer using stream_results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. To enable server side cursors without a specific partition size, the :paramref:`_engine.Connection.execution_options.stream_results` option may be used, which like :paramref:`_engine.Connection.execution_options.yield_per` may be called on the :class:`_engine.Connection` object or the statement object.

特定のパーティションサイズを持たないサーバ側カーソルを有効にするには、 :paramref:`_engine.Connection.execution_options.stream_results` オプションを使用します。これは、 :paramref:`_engine.Connection.execution_options.yield_per` と同様に、 :class:`_engine.Connection` オブジェクトまたはステートメントオブジェクトで呼び出すことができます。

.. When a :class:`_engine.Result` object delivered using the :paramref:`_engine.Connection.execution_options.stream_results` option is iterated directly, rows are fetched internally using a default buffering scheme that buffers first a small set of rows, then a larger and larger buffer on each fetch up to a pre-configured limit of 1000 rows.   The maximum size of this buffer can be affected using the :paramref:`_engine.Connection.execution_options.max_row_buffer` execution option::

:paramref:`_engine.Connection.execution_options.stream_results` オプションを使用して配信された :class:`_engine.Result` オブジェクトが直接反復される場合、行はデフォルトのバッファリング方式を使用して内部的にフェッチされます。この方式では、最初に小さな行のセットがバッファリングされ、次に、事前に設定された1,000行の制限まで、各フェッチでより大きなバッファがバッファリングされます。このバッファの最大サイズは、 :paramref:`_engine.Connection.execution_options.max_row_buffer` 実行オプションを使用して変更できます::

    with engine.connect() as conn:
        with conn.execution_options(stream_results=True, max_row_buffer=100).execute(
            text("select * from table")
        ) as result:
            for row in result:
                print(f"{row}")

.. While the :paramref:`_engine.Connection.execution_options.stream_results` option may be combined with use of the :meth:`_engine.Result.partitions` method, a specific partition size should be passed to :meth:`_engine.Result.partitions` so that the entire result is not fetched.  It is usually more straightforward to use the :paramref:`_engine.Connection.execution_options.yield_per` option when setting up to use the :meth:`_engine.Result.partitions` method.

:paramref:`_engine.Connection.execution_options.stream_results` オプションは :meth:`_engine.Result.partitions` メソッドの使用と組み合わせることができますが、結果全体がフェッチされないように、特定のパーティションサイズを :meth:`_engine.Result.partitions` に渡す必要があります。通常、 :meth:`_engine.Result.partitions` メソッドを使用するように設定する場合は、 :paramref:`_engine.Connection.execution_options.yield_per` オプションを使用する方が簡単です。

.. seealso::

    :ref:`orm_queryguide_yield_per` - in the :ref:`queryguide_toplevel`

    :meth:`_engine.Result.partitions`

    :meth:`_engine.Result.yield_per`


.. _schema_translating:

Translation of Schema Names
---------------------------

.. To support multi-tenancy applications that distribute common sets of tables into multiple schemas, the :paramref:`.Connection.execution_options.schema_translate_map` execution option may be used to repurpose a set of :class:`_schema.Table` objects to render under different schema names without any changes.

共通のテーブルセットを複数のスキーマに分散するマルチテナンシアプリケーションをサポートするために、 :paramref:`.Connection.execution_options.schema_translate_map` 実行オプションを使用して、 :class:`_schema.Table` オブジェクトのセットを変更せずに別のスキーマ名でレンダリングすることができます。

Given a table::

    user_table = Table(
        "user",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )

.. The "schema" of this :class:`_schema.Table` as defined by the :paramref:`_schema.Table.schema` attribute is ``None``.  The :paramref:`.Connection.execution_options.schema_translate_map` can specify that all :class:`_schema.Table` objects with a schema of ``None`` would instead render the schema as ``user_schema_one``::

:paramref:`_schema.Table.schema` 属性で定義されているこの :class:`_schema.Table` の"スキーマは ``None`` です。 :paramref:`.Connection.execution_options.schema_translate_map` では、 ``None`` のスキーマを持つすべての :class:`_schema.Table` オブジェクトが、代わりに ``use_schema_one`` としてスキーマを描画することを指定できます::

    connection = engine.connect().execution_options(
        schema_translate_map={None: "user_schema_one"}
    )

    result = connection.execute(user_table.select())

.. The above code will invoke SQL on the database of the form:

上記のコードは、次の形式のデータベースに対してSQLを呼び出します:

.. sourcecode:: sql

    SELECT user_schema_one.user.id, user_schema_one.user.name FROM
    user_schema_one.user

.. That is, the schema name is substituted with our translated name.  The map can specify any number of target->destination schemas::

つまり、スキーマ名は変換された名前に置き換えられます。マップには、任意の数のtarget->destinationスキーマを指定できます::

    connection = engine.connect().execution_options(
        schema_translate_map={
            None: "user_schema_one",  # no schema name -> "user_schema_one"
            "special": "special_schema",  # schema="special" becomes "special_schema"
            "public": None,  # Table objects with schema="public" will render with no schema
        }
    )

.. The :paramref:`.Connection.execution_options.schema_translate_map` parameter affects all DDL and SQL constructs generated from the SQL expression language, as derived from the :class:`_schema.Table` or :class:`.Sequence` objects.  It does **not** impact literal string SQL used via the :func:`_expression.text` construct nor via plain strings passed to :meth:`_engine.Connection.execute`.

:paramref:`.Connection.execution_options.schema_translate_map` パラメータは、 :class:`_schema.Table` または :class:`.Sequence` オブジェクトから派生した、SQL式言語から生成されたすべてのDDLおよびSQL構文に影響します。 :func:`_expression.text` 構文または :meth:`_engine.Connection.execute` に渡されたプレーンな文字列を介して使用されるリテラル文字列SQLには影響 **しません** 。

.. The feature takes effect **only** in those cases where the name of the schema is derived directly from that of a :class:`_schema.Table` or :class:`.Sequence`; it does not impact methods where a string schema name is passed directly.  By this pattern, it takes effect within the "can create" / "can drop" checks performed by methods such as :meth:`_schema.MetaData.create_all` or :meth:`_schema.MetaData.drop_all` are called, and it takes effect when using table reflection given a :class:`_schema.Table` object.  However it does **not** affect the operations present on the :class:`_reflection.Inspector` object, as the schema name is passed to these methods explicitly.

この機能は、スキーマの名前が :class:`_schema.Table` または :class:`.Sequence` の名前から直接派生している場合に **のみ** 有効です。文字列スキーマ名が直接渡されるメソッドには影響しません。このパターンでは、 :meth:`_schema.MetaData.create_all` や :meth:`_schema.MetaData.drop_all `などのメソッドによって実行される"can create" / "can drop"チェック内で有効になり、 :class:`_schema.Table` オブジェクトを指定してテーブルリフレクションを使用するときに有効になります。ただし、スキーマ名がこれらのメソッドに明示的に渡されるので 、:class:`_reflection.Inspector` オブジェクトに存在する操作には **影響しません** 。

.. tip::

    .. To use the schema translation feature with the ORM :class:`_orm.Session`, set this option at the level of the :class:`_engine.Engine`, then pass that engine to the :class:`_orm.Session`.  The :class:`_orm.Session` uses a new :class:`_engine.Connection` for each transaction::

    ORM :class:`_orm.Session`で スキーマ変換機能を使用するには、このオプションを :class:`_engine.Engine` のレベルで設定してから、そのエンジンを :class:`_orm.Session` に渡します。 :class:`_orm.Session` はトランザクションごとに新しい :class:`_engine.Connection` を使用します::

      schema_engine = engine.execution_options(schema_translate_map={...})

      session = Session(schema_engine)

      ...

  .. warning::

    .. When using the ORM :class:`_orm.Session` without extensions, the schema translate feature is only supported as **a single schema translate map per Session**.   It will **not work** if different schema translate maps are given on a per-statement basis, as the ORM :class:`_orm.Session` does not take current schema translate values into account for individual objects.

    ORM :class:`_orm.Session` を拡張なしで使用する場合、スキーマ変換機能は **セッションごとに1つのスキーマ変換マップ** としてのみサポートされます。ORM :class:`_orm.Session` は現在のスキーマ変換値を個々のオブジェクトに対して考慮しないため、異なるスキーマ変換マップが文ごとに指定されている場合は **機能しません** 。

    .. To use a single :class:`_orm.Session` with multiple ``schema_translate_map`` configurations, the :ref:`horizontal_sharding_toplevel` extension may be used.  See the example at :ref:`examples_sharding`.

    単一の :class:`_orm.Session` を複数の `schema_translate_map` 設定で使用するには、 :ref:`horizontal_sharding_toplevel` 拡張を使用できます。 :ref:`examples_sharding` の例を参照してください。

.. _sql_caching:


SQL Compilation Caching
-----------------------

.. .. versionadded:: 1.4  SQLAlchemy now has a transparent query caching system that substantially lowers the Python computational overhead involved in converting SQL statement constructs into SQL strings across both Core and ORM.   See the introduction at :ref:`change_4639`.

.. versionadded:: 1.4 SQLAlchemyに透過的なクエリキャッシュシステムが追加されました。これにより、CoreとORMの両方で、SQL文の構成をSQL文字列に変換する際のPythonの計算オーバーヘッドが大幅に削減されます。 :ref:`change_4639` の導入部分を参照してください。

.. SQLAlchemy includes a comprehensive caching system for the SQL compiler as well as its ORM variants.   This caching system is transparent within the :class:`.Engine` and provides that the SQL compilation process for a given Core or ORM SQL statement, as well as related computations which assemble result-fetching mechanics for that statement, will only occur once for that statement object and all others with the identical structure, for the duration that the particular structure remains within the engine's "compiled cache". By "statement objects that have the identical structure", this generally corresponds to a SQL statement that is constructed within a function and is built each time that function runs::

SQLAlchemyには、SQLコンパイラとそのORMバリアントのための包括的なキャッシュシステムが含まれています。このキャッシュシステムは :class:`.Engine` 内で透過的であり、特定のCoreまたはORM SQLステートメントのSQLコンパイルプロセスと、そのステートメントの結果フェッチ機構を組み立てる関連計算が、エンジンの"コンパイルされたキャッシュ"内に特定の構造が残っている間、そのステートメントオブジェクトと同じ構造を持つ他のすべてのオブジェクトに対して一度だけ発生することを提供します。「同じ構造を持つステートメントオブジェクト」とは、一般に、関数内で構築され、その関数が実行されるたびに構築されるSQLステートメントに対応します::

    def run_my_statement(connection, parameter):
        stmt = select(table)
        stmt = stmt.where(table.c.col == parameter)
        stmt = stmt.order_by(table.c.id)
        return connection.execute(stmt)

.. The above statement will generate SQL resembling ``SELECT id, col FROM table WHERE col = :col ORDER BY id``, noting that while the value of ``parameter`` is a plain Python object such as a string or an integer, the string SQL form of the statement does not include this value as it uses bound parameters.  Subsequent invocations of the above ``run_my_statement()`` function will use a cached compilation construct within the scope of the ``connection.execute()`` call for enhanced performance.

上の文は、 ``SELECT id, col FROM table WHERE col = :col ORDER BY id`` のようなSQLを生成します。ただし、 ``parameter`` の値は文字列や整数などのプレーンなPythonオブジェクトですが、バインドされたパラメータを使用するため、文字列のSQL形式の文にはこの値が含まれません。上記の ``run_my_statement()`` 関数の後続の呼び出しでは、パフォーマンスを向上させるために ``connection.execute()`` 呼び出しの範囲内でキャッシュされたコンパイル構文が使用されます。

.. .. note:: it is important to note that the SQL compilation cache is caching the **SQL string that is passed to the database only**, and **not the data** returned by a query.   It is in no way a data cache and does not impact the results returned for a particular SQL statement nor does it imply any memory use linked to fetching of result rows.

.. note:: SQLコンパイルキャッシュがキャッシュしているのは、データベースに渡された **SQL文字列のみ** であり、 **クエリによって返されたデータ** ではないことに注意してください。これは決してデータキャッシュではなく、特定のSQL文に対して返された結果に影響を与えず、結果行のフェッチに関連したメモリの使用を意味しません。

.. While SQLAlchemy has had a rudimentary statement cache since the early 1.x series, and additionally has featured the "Baked Query" extension for the ORM, both of these systems required a high degree of special API use in order for the cache to be effective.  The new cache as of 1.4 is instead completely automatic and requires no change in programming style to be effective.

SQLAlchemyは初期の1.xシリーズから初歩的なステートメントキャッシュを持っており、さらにORMのための"Baked Query"拡張を特徴としているが、これらのシステムは両方とも、キャッシュを効果的にするために高度な特別なAPI使用を必要とした。1.4年の新しいキャッシュは完全に自動的であり、効果的にするためにプログラミングスタイルを変更する必要はない。

.. The cache is automatically used without any configurational changes and no special steps are needed in order to enable it. The following sections detail the configuration and advanced usage patterns for the cache.

キャッシュは構成を変更せずに自動的に使用されるため、キャッシュを有効にするための特別な手順は必要ありません。次のセクションでは、キャッシュの構成と高度な使用パターンについて詳しく説明します。


Configuration
~~~~~~~~~~~~~

.. The cache itself is a dictionary-like object called an ``LRUCache``, which is an internal SQLAlchemy dictionary subclass that tracks the usage of particular keys and features a periodic "pruning" step which removes the least recently used items when the size of the cache reaches a certain threshold.  The size of this cache defaults to 500 and may be configured using the :paramref:`_sa.create_engine.query_cache_size` parameter::

キャッシュ自体は、 ``LRUCache`` と呼ばれる辞書のようなオブジェクトです。これは、特定のキーの使用を追跡し、キャッシュのサイズが特定のしきい値に達したときに最も使用されていない項目を削除する定期的な"プルーニング"ステップを特徴とする内部SQLAlchemy辞書サブクラスです。このキャッシュのサイズはデフォルトで500で、 :paramref:`_sa.create_engine.query_cache_size` パラメータを使用して設定できます::

    engine = create_engine(
        "postgresql+psycopg2://scott:tiger@localhost/test", query_cache_size=1200
    )

.. The size of the cache can grow to be a factor of 150% of the size given, before it's pruned back down to the target size.  A cache of size 1200 above can therefore grow to be 1800 elements in size at which point it will be pruned to 1200.

キャッシュのサイズは、ターゲットサイズに縮小される前に、指定されたサイズの150%の係数になるように大きくすることができます。したがって、サイズ1200以上のキャッシュは、サイズが1800要素になるように大きくすることができ、その時点で1200に縮小されます。

.. The sizing of the cache is based on a single entry per unique SQL statement rendered, per engine.   SQL statements generated from both the Core and the ORM are treated equally.  DDL statements will usually not be cached.  In order to determine what the cache is doing, engine logging will include details about the cache's behavior, described in the next section.

 キャッシュのサイズ設定は、エンジンごとにレンダリングされる一意のSQL文ごとに1つのエントリに基づいて行われます。コアとORMの両方から生成されたSQL文は同等に扱われます。通常、DDL文はキャッシュされません。キャッシュが何を行っているかを判断するために、エンジンロギングには、次のセクションで説明するキャッシュの動作に関する詳細が含まれます。

.. _sql_caching_logging:

Estimating Cache Performance Using Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The above cache size of 1200 is actually fairly large.   For small applications, a size of 100 is likely sufficient.  To estimate the optimal size of the cache, assuming enough memory is present on the target host, the size of the cache should be based on the number of unique SQL strings that may be rendered for the target engine in use.    The most expedient way to see this is to use SQL echoing, which is most directly enabled by using the :paramref:`_sa.create_engine.echo` flag, or by using Python logging; see the section :ref:`dbengine_logging` for background on logging configuration.

上記のキャッシュサイズ1200は、実際にはかなり大きくなります。小規模なアプリケーションでは、100のサイズで十分です。キャッシュの最適なサイズを推定するには、ターゲットホストに十分なメモリが存在すると仮定して、キャッシュのサイズは、使用中のターゲットエンジンに対してレンダリングされる一意のSQL文字列の数に基づく必要があります。これを確認する最も便利な方法は、SQLエコーを使用することです。これは、 :paramref:`_sa.create_engine.echo` フラグを使用するか、Pythonロギングを使用することによって、最も直接的に有効になります。ロギング設定の背景については、 :ref:`dbengine_logging` のセクションを参照してください。

.. As an example, we will examine the logging produced by the following program::

例として、次のプログラムによって生成されたログを調べます::

    from sqlalchemy import Column
    from sqlalchemy import create_engine
    from sqlalchemy import ForeignKey
    from sqlalchemy import Integer
    from sqlalchemy import select
    from sqlalchemy import String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship
    from sqlalchemy.orm import Session

    Base = declarative_base()


    class A(Base):
        __tablename__ = "a"

        id = Column(Integer, primary_key=True)
        data = Column(String)
        bs = relationship("B")


    class B(Base):
        __tablename__ = "b"
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey("a.id"))
        data = Column(String)


    e = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(e)

    s = Session(e)

    s.add_all([A(bs=[B(), B(), B()]), A(bs=[B(), B(), B()]), A(bs=[B(), B(), B()])])
    s.commit()

    for a_rec in s.scalars(select(A)):
        print(a_rec.bs)

.. When run, each SQL statement that's logged will include a bracketed cache statistics badge to the left of the parameters passed.   The four types of message we may see are summarized as follows:

実行されると、ログに記録される各SQL文には、渡されたパラメータの左側に括弧で囲まれたキャッシュ統計バッジが含まれます。表示される可能性のある4つのタイプのメッセージは、次のように要約されます。

.. * ``[raw sql]`` - the driver or the end-user emitted raw SQL using :meth:`.Connection.exec_driver_sql` - caching does not apply

* ``[raw sql]`` - ドライバまたはエンドユーザが :meth:`.Connection.exec_driver_sql` を使用して生のSQLを発行しました - キャッシュは適用されません

.. * ``[no key]`` - the statement object is a DDL statement that is not cached, or the statement object contains uncacheable elements such as user-defined constructs or arbitrarily large VALUES clauses.

* ``[no key]`` - 文オブジェクトがキャッシュされていないDDL文であるか、ユーザ定義の構文や任意の大きさのVALUES句など、キャッシュできない要素が文オブジェクトに含まれています。

.. * ``[generated in Xs]`` - the statement was a **cache miss** and had to be compiled, then stored in the cache.  it took X seconds to produce the compiled construct.  The number X will be in the small fractional seconds.

* ``[generated in Xs]`` - この文は **キャッシュミス** であり、コンパイルされてからキャッシュに格納される必要がありました。コンパイルされた構文を生成するのにX秒かかりました。数値Xは小数点以下の秒数になります。

.. * ``[cached since Xs ago]`` - the statement was a **cache hit** and did not have to be recompiled.  The statement has been stored in the cache since X seconds ago.  The number X will be proportional to how long the application has been running and how long the statement has been cached, so for example would be 86400 for a 24 hour period.

* ``[cached since Xs ago]`` - 文は **キャッシュヒット** であり、再コンパイルする必要はありませんでした。文はX秒前からキャッシュに保存されています。Xという数字は、アプリケーションが実行されていた時間と文がキャッシュされていた時間に比例します。たとえば、24時間の場合は86400になります。

.. Each badge is described in more detail below.

各バッジについては、以下で詳しく説明します。

.. The first statements we see for the above program will be the SQLite dialect checking for the existence of the "a" and "b" tables:

上記のプログラムで最初に表示される文は、"a"テーブルと"b"テーブルの存在をチェックするSQLiteダイアレクトです:

.. sourcecode:: text

  INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("a")
  INFO sqlalchemy.engine.Engine [raw sql] ()
  INFO sqlalchemy.engine.Engine PRAGMA main.table_info("b")
  INFO sqlalchemy.engine.Engine [raw sql] ()

.. For the above two SQLite PRAGMA statements, the badge reads ``[raw sql]``, which indicates the driver is sending a Python string directly to the database using :meth:`.Connection.exec_driver_sql`.  Caching does not apply to such statements because they already exist in string form, and there is nothing known about what kinds of result rows will be returned since SQLAlchemy does not parse SQL strings ahead of time.

上記の2つのSQLite PRAGMA文の場合、バッジには ``[raw sql]`` と表示されます。これは、ドライバが :meth:`.Connection.exec_driver_sql` を使用してPython文字列を直接データベースに送信していることを示します。このような文は既に文字列形式で存在するため、キャッシュは適用されません。また、SQLAlchemyは事前にSQL文字列を解析しないため、どのような種類の結果行が返されるかについては何もわかりません。

.. The next statements we see are the CREATE TABLE statements:

次の文は、CREATE TABLE文です:

.. sourcecode:: sql

  INFO sqlalchemy.engine.Engine
  CREATE TABLE a (
    id INTEGER NOT NULL,
    data VARCHAR,
    PRIMARY KEY (id)
  )

  INFO sqlalchemy.engine.Engine [no key 0.00007s] ()
  INFO sqlalchemy.engine.Engine
  CREATE TABLE b (
    id INTEGER NOT NULL,
    a_id INTEGER,
    data VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY(a_id) REFERENCES a (id)
  )

  INFO sqlalchemy.engine.Engine [no key 0.00006s] ()

.. For each of these statements, the badge reads ``[no key 0.00006s]``.  This indicates that these two particular statements, caching did not occur because the DDL-oriented :class:`_schema.CreateTable` construct did not produce a cache key.  DDL constructs generally do not participate in caching because they are not typically subject to being repeated a second time and DDL is also a database configurational step where performance is not as critical.

これらの文のそれぞれに対して、バッジには ``[no key 0.00006s]`` と書かれています。これは、DDL指向の :class:`_schema.CreateTable` 構文がキャッシュキーを生成しなかったために、これら2つの特定の文のキャッシュが行われなかったことを示しています。DDL構文は通常、2回目の繰り返しの対象にならないため、キャッシュには関与しません。また、DDLはパフォーマンスがそれほど重要ではないデータベース構成ステップでもあるためです。

.. The ``[no key]`` badge is important for one other reason, as it can be produced for SQL statements that are cacheable except for some particular sub-construct that is not currently cacheable.   Examples of this include custom user-defined SQL elements that don't define caching parameters, as well as some constructs that generate arbitrarily long and non-reproducible SQL strings, the main examples being the :class:`.Values` construct as well as when using "multivalued inserts" with the :meth:`.Insert.values` method.

``[no key]`` バッジが重要な理由はもう1つあります。これは、現在キャッシュできない特定のサブ構文を除いて、キャッシュできるSQL文に対して生成される可能性があるためです。この例としては、キャッシュパラメータを定義しないカスタムのユーザ定義SQL要素や、任意の長さで再現性のないSQL文字列を生成するいくつかの構文があります。主な例としては、 :class:`.Values` 構文や、 :meth:`.Insert.values` メソッドで「複数値の挿入」を使用する場合などです。

.. So far our cache is still empty.  The next statements will be cached however, a segment looks like:

これまでのところ、キャッシュはまだ空です。次の文はキャッシュされますが、セグメントは次のようになります。

.. sourcecode:: sql

  INFO sqlalchemy.engine.Engine INSERT INTO a (data) VALUES (?)
  INFO sqlalchemy.engine.Engine [generated in 0.00011s] (None,)
  INFO sqlalchemy.engine.Engine INSERT INTO a (data) VALUES (?)
  INFO sqlalchemy.engine.Engine [cached since 0.0003533s ago] (None,)
  INFO sqlalchemy.engine.Engine INSERT INTO a (data) VALUES (?)
  INFO sqlalchemy.engine.Engine [cached since 0.0005326s ago] (None,)
  INFO sqlalchemy.engine.Engine INSERT INTO b (a_id, data) VALUES (?, ?)
  INFO sqlalchemy.engine.Engine [generated in 0.00010s] (1, None)
  INFO sqlalchemy.engine.Engine INSERT INTO b (a_id, data) VALUES (?, ?)
  INFO sqlalchemy.engine.Engine [cached since 0.0003232s ago] (1, None)
  INFO sqlalchemy.engine.Engine INSERT INTO b (a_id, data) VALUES (?, ?)
  INFO sqlalchemy.engine.Engine [cached since 0.0004887s ago] (1, None)

.. Above, we see essentially two unique SQL strings; ``"INSERT INTO a (data) VALUES (?)"`` and ``"INSERT INTO b (a_id, data) VALUES (?, ?)"``.  Since SQLAlchemy uses bound parameters for all literal values, even though these statements are repeated many times for different objects, because the parameters are separate, the actual SQL string stays the same.

上記の例では、基本的に2つのユニークなSQL文字列、すなわち ``"INSERT INTO a(data) VALUES(?)"`` と ``"INSERT INTO b (a_id, data) VALUES(?,?)"`` があります。SQLAlchemyは全てのリテラル値にバウンドパラメータを使用するので、これらの文が異なるオブジェクトに対して何度も繰り返されても、パラメータが分離されているので、実際のSQL文字列は同じままです。

.. .. note:: the above two statements are generated by the ORM unit of work process, and in fact will be caching these in a separate cache that is local to each mapper.  However the mechanics and terminology are the same.  The section :ref:`engine_compiled_cache` below will describe how user-facing code can also use an alternate caching container on a per-statement basis.

.. note:: 上記の2つのステートメントは、ORMの作業単位プロセスによって生成され、実際には、各マッパーに対して行カルな個別のキャッシュにこれらをキャッシュします。ただし、仕組みと用語は同じです。以下のセクション :ref:`engine_compiled_cache` では、ユーザー向けコードがステートメントごとに代替キャッシュコンテナを使用する方法について説明します。

.. The caching badge we see for the first occurrence of each of these two statements is ``[generated in 0.00011s]``. This indicates that the statement was **not in the cache, was compiled into a String in .00011s and was then cached**.   When we see the ``[generated]`` badge, we know that this means there was a **cache miss**.  This is to be expected for the first occurrence of a particular statement.  However, if lots of new ``[generated]`` badges are observed for a long-running application that is generally using the same series of SQL statements over and over, this may be a sign that the :paramref:`_sa.create_engine.query_cache_size` parameter is too small.  When a statement that was cached is then evicted from the cache due to the LRU cache pruning lesser used items, it will display the ``[generated]`` badge when it is next used.

これらの2つの文の最初の出現に対して表示されるキャッシュバッジは、 ``[generated in 0.00011s]`` です。これは、文が **キャッシュ内になく、.00011sで文字列にコンパイルされ、その後キャッシュされた** ことを示します。 ``[generated]`` バッジを見ると、これは **キャッシュミス** があったことを意味していることがわかります。これは、特定の文の最初の出現に対して予想されることです。しかし、一般的に同じ一連のSQL文を何度も使用している長時間実行されるアプリケーションに対して、多くの新しい ``[generated]`` バッジが観察される場合、これは :paramref:`_sa.create_engine.query_cache_size` パラメータが小さすぎることを示している可能性があります。キャッシュされた文が、LRUキャッシュの使用頻度の低い項目のプルーニングによりキャッシュから削除されると、次に使用されるときに ``[generated]`` バッジが表示されます。

.. The caching badge that we then see for the subsequent occurrences of each of these two statements looks like ``[cached since 0.0003533s ago]``.  This indicates that the statement **was found in the cache, and was originally placed into the cache .0003533 seconds ago**.   It is important to note that while the ``[generated]`` and ``[cached since]`` badges refer to a number of seconds, they mean different things; in the case of ``[generated]``, the number is a rough timing of how long it took to compile the statement, and will be an extremely small amount of time.   In the case of ``[cached since]``, this is the total time that a statement has been present in the cache.  For an application that's been running for six hours, this number may read ``[cached since 21600 seconds ago]``, and that's a good thing.    Seeing high numbers for "cached since" is an indication that these statements have not been subject to cache misses for a long time.  Statements that frequently have a low number of "cached since" even if the application has been running a long time may indicate these statements are too frequently subject to cache misses, and that the :paramref:`_sa.create_engine.query_cache_size` may need to be increased.

これら2つの文のそれぞれの後続の出現に対して表示されるキャッシュバッジは、 ``[cached since 0.0003533s ago]`` のようになります。これは、文 **がキャッシュ内で検出され、元々キャッシュ内に0003533秒前に置かれていたことを示します** 。 ``[generated]`` バッジと ``[cached since]`` バッジは秒数を表しますが、意味は異なります。 ``[generated]`` バッジの場合、秒数は文のコンパイルにかかった時間の大まかなタイミングであり、非常に短い時間になります。 ``[cached since]`` の場合、これは文がキャッシュ内に存在していた合計時間です。6時間実行されているアプリケーションの場合、この数値は ``[cached since 21600 seconds ago]`` と表示されます。これは良いことです。"cached since"の値が大きい場合は、これらの文が長い間キャッシュ・ミスの対象になっていないことを示しています。アプリケーションが長時間実行されていても、"cached since"の数が少ない文は、これらの文がキャッシュミスを頻繁に起こし、 :paramref:`_sa.create_engine.query_cache_size` を増やす必要があることを示している可能性があります。

.. Our example program then performs some SELECTs where we can see the same pattern of "generated" then "cached", for the SELECT of the "a" table as well as for subsequent lazy loads of the "b" table:

次に、この例のプログラムでは、"a"テーブルのSELECTと、それに続く"b"テーブルの遅延行ドに対して、"generated"と"cached"の同じパターンが見られるいくつかのSELECTを実行します:

.. sourcecode:: text

  INFO sqlalchemy.engine.Engine SELECT a.id AS a_id, a.data AS a_data
  FROM a
  INFO sqlalchemy.engine.Engine [generated in 0.00009s] ()
  INFO sqlalchemy.engine.Engine SELECT b.id AS b_id, b.a_id AS b_a_id, b.data AS b_data
  FROM b
  WHERE ? = b.a_id
  INFO sqlalchemy.engine.Engine [generated in 0.00010s] (1,)
  INFO sqlalchemy.engine.Engine SELECT b.id AS b_id, b.a_id AS b_a_id, b.data AS b_data
  FROM b
  WHERE ? = b.a_id
  INFO sqlalchemy.engine.Engine [cached since 0.0005922s ago] (2,)
  INFO sqlalchemy.engine.Engine SELECT b.id AS b_id, b.a_id AS b_a_id, b.data AS b_data
  FROM b
  WHERE ? = b.a_id

.. From our above program, a full run shows a total of four distinct SQL strings being cached.   Which indicates a cache size of **four** would be sufficient.   This is obviously an extremely small size, and the default size of 500 is fine to be left at its default.

上記のプログラムから、完全な実行では、合計4つの異なるSQL文字列がキャッシュされていることが示されます。これは、 **4** のキャッシュ・サイズで十分であることを示しています。これは明らかに非常に小さいサイズであり、デフォルトのサイズ500はデフォルトのままで問題ありません。

How much memory does the cache use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The previous section detailed some techniques to check if the :paramref:`_sa.create_engine.query_cache_size` needs to be bigger.   How do we know if the cache is not too large?   The reason we may want to set :paramref:`_sa.create_engine.query_cache_size` to not be higher than a certain number would be because we have an application that may make use of a very large number of different statements, such as an application that is building queries on the fly from a search UX, and we don't want our host to run out of memory if for example, a hundred thousand different queries were run in the past 24 hours and they were all cached.

前のセクションでは、 :paramref:`_sa.create_engine.query_cache_size` を大きくする必要があるかどうかをチェックするいくつかのテクニックについて詳しく説明しました。キャッシュが大きすぎないかどうかはどうすればわかりますか? :paramref:`_sa.create_engine.query_cache_size` を特定の数より大きくしないように設定したい理由は、検索UXからオンザフライでクエリを構築するアプリケーションなど、非常に多数の異なるステートメントを使用する可能性のあるアプリケーションがあるためです。また、たとえば、過去24時間に10万の異なるクエリが実行され、それらがすべてキャッシュされた場合に、ホストのメモリが不足しないようにするためです。

.. It is extremely difficult to measure how much memory is occupied by Python data structures, however using a process to measure growth in memory via ``top`` as a successive series of 250 new statements are added to the cache suggest a moderate Core statement takes up about 12K while a small ORM statement takes about 20K, including result-fetching structures which for the ORM will be much greater.

Pythonのデータ構造がどれだけのメモリを占有しているかを測定するのは非常に困難ですが、 ``top`` を介してメモリの増加を測定するプロセスを使用すると、一連の250の新しいステートメントがキャッシュに追加されるため、中程度のCoreステートメントは約12Kを消費しますが、小さなORMステートメントは約20Kを消費します。これには、ORMにとってはるかに大きな結果フェッチ構造も含まれます。

.. _engine_compiled_cache:

Disabling or using an alternate dictionary to cache some (or all) statements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The internal cache used is known as ``LRUCache``, but this is mostly just a dictionary.  Any dictionary may be used as a cache for any series of statements by using the :paramref:`.Connection.execution_options.compiled_cache` option as an execution option.  Execution options may be set on a statement, on an :class:`_engine.Engine` or :class:`_engine.Connection`, as well as when using the ORM :meth:`_orm.Session.execute` method for SQLAlchemy-2.0 style invocations.   For example, to run a series of SQL statements and have them cached in a particular dictionary::

使用される内部キャッシュは ``LRUCache`` として知られていますが、これはほとんど単なる辞書です。 :paramref:`.Connection.execution_options.compiled_cache` オプションを実行オプションとして使用することで、任意の辞書を任意の一連の文のキャッシュとして使用できます。実行オプションは、ORM :meth:`_orm.Session.execute` メソッドをSQLAlchemy-2.0スタイルの呼び出しに使用する場合と同様に、文、 :class:`_engine.Engine` または :class:`_engine.Connection` に設定できます。たとえば、一連のSQL文を実行し、それらを特定の辞書にキャッシュするには::

    my_cache = {}
    with engine.connect().execution_options(compiled_cache=my_cache) as conn:
        conn.execute(table.select())

.. The SQLAlchemy ORM uses the above technique to hold onto per-mapper caches within the unit of work "flush" process that are separate from the default cache configured on the :class:`_engine.Engine`, as well as for some relationship loader queries.

SQLAlchemy ORMは上記のテクニックを使用して、 :class:`_engine.Engine` で設定されたデフォルトキャッシュとは別の、作業単位の"フラッシュ"プロセス内のマッパーごとのキャッシュを保持します。

.. The cache can also be disabled with this argument by sending a value of ``None``::

この引数に ``None`` を指定してキャッシュを無効にすることもできます::

    # disable caching for this connection
    with engine.connect().execution_options(compiled_cache=None) as conn:
        conn.execute(table.select())

.. _engine_thirdparty_caching:

Caching for Third Party Dialects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The caching feature requires that the dialect's compiler produces SQL strings that are safe to reuse for many statement invocations, given a particular cache key that is keyed to that SQL string.  This means that any literal values in a statement, such as the LIMIT/OFFSET values for a SELECT, can not be hardcoded in the dialect's compilation scheme, as the compiled string will not be re-usable.   SQLAlchemy supports rendered bound parameters using the :meth:`_sql.BindParameter.render_literal_execute` method which can be applied to the existing ``Select._limit_clause`` and ``Select._offset_clause`` attributes by a custom compiler, which are illustrated later in this section.

キャッシュ機能では、そのSQL文字列にキー付けされた特定のキャッシュキーが与えられた場合、多くの文の呼び出しで安全に再利用できるSQL文字列をダイアレクトのコンパイラが生成する必要があります。これは、SELECTのLIMIT/OFFSET値など、文の中のリテラル値は、コンパイルされた文字列が再利用できないため、ダイアレクトのコンパイルスキームでハードコードできないことを意味します。SQLAlchemyは、 :meth:`_sql.BindParameter.render_literal_execute` メソッドを使用してレンダリングされたバインドパラメータをサポートしています。このメソッドは、カスタムコンパイラによって既存の ``Select._limit_clause`` および ``Select._offset_clause`` 属性に適用できます。これらについては、このセクションの後半で説明します。

.. As there are many third party dialects, many of which may be generating literal values from SQL statements without the benefit of the newer "literal execute" feature, SQLAlchemy as of version 1.4.5 has added an attribute to dialects known as :attr:`_engine.Dialect.supports_statement_cache`. This attribute is checked at runtime for its presence directly on a particular dialect's class, even if it's already present on a superclass, so that even a third party dialect that subclasses an existing cacheable SQLAlchemy dialect such as ``sqlalchemy.dialects.postgresql.PGDialect`` must still explicitly include this attribute for caching to be enabled. The attribute should **only** be enabled once the dialect has been altered as needed and tested for reusability of compiled SQL statements with differing parameters.

多くのサードパーティのダイアレクトがあり、その多くは新しい"リテラル実行"機能の恩恵を受けずにSQL文からリテラル値を生成している可能性があるため、バージョン1.4.5のSQLAlchemyはダイアレクトに :attr:`_engine.Dialect.supports_statement_cache` として知られる属性を追加しました。この属性は、すでにスーパークラスに存在している場合でも、実行時に特定のダイアレクトのクラスに直接存在するかどうかがチェックされます。そのため、既存のキャッシュ可能なSQLAlchemyダイアレクトをサブクラス化しているサードパーティのダイアレクト(例えば``SQLAlchemy.dialects.postgresql.PGDialect``)であっても、キャッシュを有効にするためにはこの属性を明示的に含める必要があります。この属性は、ダイアレクトが必要に応じて変更され、異なるパラメータでコンパイルされたSQL文の再利用性がテストされた場合にのみ有効にする必要があります。

.. For all third party dialects that don't support this attribute, the logging for such a dialect will indicate ``dialect does not support caching``.

この属性をサポートしていないすべてのサードパーティのダイアレクトでは、そのようなダイアレクトのロギングは ``dialect does not support caching`` と表示されます。

.. When a dialect has been tested against caching, and in particular the SQL compiler has been updated to not render any literal LIMIT / OFFSET within a SQL string directly, dialect authors can apply the attribute as follows::

ダイアレクトがキャッシュに対してテストされ、特にSQLコンパイラがSQL文字列内のリテラルLIMIT/OFFSETを直接レンダリングしないように更新された場合、ダイアレクトの作成者は次のように属性を適用できます::

    from sqlalchemy.engine.default import DefaultDialect

    class MyDialect(DefaultDialect):
        supports_statement_cache = True

.. The flag needs to be applied to all subclasses of the dialect as well::

このフラグは、ダイアレクトのすべてのサブクラスにも適用する必要があります::

    class MyDBAPIForMyDialect(MyDialect):
        supports_statement_cache = True

.. .. versionadded:: 1.4.5 Added the :attr:`.Dialect.supports_statement_cache` attribute.

.. versionadded:: 1.4.5 :attr:`.Dialect.supports_statement_cache` 属性を追加しました。

The typical case for dialect modification follows.

特殊なケースの修正の典型的な例を次に示します。

Example: Rendering LIMIT / OFFSET with post compile parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. As an example, suppose a dialect overrides the :meth:`.SQLCompiler.limit_clause` method, which produces the "LIMIT / OFFSET" clause for a SQL statement, like this::

例として、ある書き方が :meth:`.SQLCompiler.limit_clause` メソッドをオーバーライドし、次のようにSQL文の"LIMIT / OFFSET"句を生成するとします::

    # pre 1.4 style code
    def limit_clause(self, select, **kw):
        text = ""
        if select._limit is not None:
            text += " \n LIMIT %d" % (select._limit,)
        if select._offset is not None:
            text += " \n OFFSET %d" % (select._offset,)
        return text

.. The above routine renders the :attr:`.Select._limit` and :attr:`.Select._offset` integer values as literal integers embedded in the SQL statement. This is a common requirement for databases that do not support using a bound parameter within the LIMIT/OFFSET clauses of a SELECT statement.  However, rendering the integer value within the initial compilation stage is directly **incompatible** with caching as the limit and offset integer values of a :class:`.Select` object are not part of the cache key, so that many :class:`.Select` statements with different limit/offset values would not render with the correct value.

上記のルーチンは、 :attr:`.Select._limit` および :attr:`.Select._offset` の整数値をSQL文に埋め込まれたリテラル整数としてレンダリングします。これは、SELECT文のLIMIT/OFFSET句内でのバウンドパラメータの使用をサポートしていないデータベースの一般的な要件です。しかし、初期コンパイル段階で整数値をレンダリングすることは、キャッシュと直接 **互換性がありません** 。 :class:`.Select` オブジェクトの制限整数値とオフセット整数値はキャッシュキーの一部ではないため、異なる制限/オフセット値を持つ多くの :class:`.Select` 文は正しい値でレンダリングされません。

.. The correction for the above code is to move the literal integer into SQLAlchemy's :ref:`post-compile <change_4808>` facility, which will render the literal integer outside of the initial compilation stage, but instead at execution time before the statement is sent to the DBAPI.  This is accessed within the compilation stage using the :meth:`_sql.BindParameter.render_literal_execute` method, in conjunction with using the :attr:`.Select._limit_clause` and :attr:`.Select._offset_clause` attributes, which represent the LIMIT/OFFSET as a complete SQL expression, as follows::

上記のコードを修正するには、リテラル整数をSQLAlchemyの :ref:`post-compile <change_4808>` 機能に移動します。これにより、リテラル整数は最初のコンパイル段階の外でレンダリングされますが、実行時には文がDBAPIに送信される前にレンダリングされます。これには、コンパイル段階で :meth:`_sql.BindParameter.render_literal_execute` メソッドを使用し、同時に :attr:`.Select._limit_clause` および :attr:`.Select._offset_clause` 属性を使用してアクセスします。これらの属性は、次のようにLIMIT/OFFSETを完全なSQL式として表します::

    # 1.4 cache-compatible code
    def limit_clause(self, select, **kw):
        text = ""

        limit_clause = select._limit_clause
        offset_clause = select._offset_clause

        if select._simple_int_clause(limit_clause):
            text += " \n LIMIT %s" % (
                self.process(limit_clause.render_literal_execute(), **kw)
            )
        elif limit_clause is not None:
            # assuming the DB doesn't support SQL expressions for LIMIT.
            # Otherwise render here normally
            raise exc.CompileError(
                "dialect 'mydialect' can only render simple integers for LIMIT"
            )
        if select._simple_int_clause(offset_clause):
            text += " \n OFFSET %s" % (
                self.process(offset_clause.render_literal_execute(), **kw)
            )
        elif offset_clause is not None:
            # assuming the DB doesn't support SQL expressions for OFFSET.
            # Otherwise render here normally
            raise exc.CompileError(
                "dialect 'mydialect' can only render simple integers for OFFSET"
            )

        return text

.. The approach above will generate a compiled SELECT statement that looks like:

上記の方法では、次のようなコンパイル済みのSELECT文が生成されます。

.. sourcecode:: sql

    SELECT x FROM y
    LIMIT __[POSTCOMPILE_param_1]
    OFFSET __[POSTCOMPILE_param_2]

.. Where above, the ``__[POSTCOMPILE_param_1]`` and ``__[POSTCOMPILE_param_2]`` indicators will be populated with their corresponding integer values at statement execution time, after the SQL string has been retrieved from the cache.

上記の場合、 ``__[POSTCOMPILE_param_1]`` および ``__[POSTCOMPILE_param_2]`` インジケータには、SQL文字列がキャッシュから取得された後、文の実行時に対応する整数値が設定されます。

.. After changes like the above have been made as appropriate, the :attr:`.Dialect.supports_statement_cache` flag should be set to ``True``.  It is strongly recommended that third party dialects make use of the `dialect third party test suite <https://github.com/sqlalchemy/sqlalchemy/blob/main/README.dialects.rst>`_ which will assert that operations like SELECTs with LIMIT/OFFSET are correctly rendered and cached.

上記のような変更が適切に行われた後、 :attr:`.Dialect.supports_statement_cache` フラグを ``True`` に設定する必要があります。サードパーティのダイアレクトでは、 `dialect third party test suite <https://github.com/sqlalchemy/sqlalchemy/blob/main/README.jpn.rst>`_ を使用することを強くお勧めします。これは、LIMIT/OFFSETを使用したSELECTのような操作が正しくレンダリングされ、キャッシュされることを主張します。

.. seealso::

    :ref:`faq_new_caching` - in the :ref:`faq_toplevel` section

.. _engine_lambda_caching:

Using Lambdas to add significant speed gains to statement production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. .. deepalchemy:: This technique is generally non-essential except in very performance intensive scenarios, and intended for experienced Python programmers.  While fairly straightforward, it involves metaprogramming concepts that are not appropriate for novice Python developers.  The lambda approach can be applied to at a later time to existing code with a minimal amount of effort.

.. deepalchemy:: このテクニックは、非常にパフォーマンス集約的なシナリオを除いて、一般的に必須ではなく、経験豊富なPythonプログラマを対象としています。かなり単純ですが、初心者のPython開発者には適していないメタプログラミングの概念を含んでいます。lambdaアプ行チは、最小限の労力で、後で既存のコードに適用できます。

.. Python functions, typically expressed as lambdas, may be used to generate SQL expressions which are cacheable based on the Python code location of the lambda function itself as well as the closure variables within the lambda.   The rationale is to allow caching of not only the SQL string-compiled form of a SQL expression construct as is SQLAlchemy's normal behavior when the lambda system isn't used, but also the in-Python composition of the SQL expression construct itself, which also has some degree of Python overhead.

一般的にlambdaとして表現されるPython関数は、lambda関数自体のPythonコードの場所とlambda内のク行ジャー変数に基づいてキャッシュ可能なSQL式を生成するために使用できます。その理論的根拠は、lambdaシステムが使用されていない場合のSQLAlchemyの通常の動作のように、SQL文字列でコンパイルされた形式のSQL式構文だけでなく、SQL式構文自体のPython内での構成もキャッシュできるようにすることであり、これにもある程度のPythonオーバーヘッドがあります。

.. The lambda SQL expression feature is available as a performance enhancing feature, and is also optionally used in the :func:`_orm.with_loader_criteria` ORM option in order to provide a generic SQL fragment.

lambda SQL式機能は、パフォーマンスを向上させる機能として使用できます。また、一般的なSQLフラグメントを提供するために、 :func:`_orm.with_loader_criteria` ORMオプションでもオプションで使用されます。

Synopsis
^^^^^^^^

.. Lambda statements are constructed using the :func:`_sql.lambda_stmt` function, which returns an instance of :class:`_sql.StatementLambdaElement`, which is itself an executable statement construct.    Additional modifiers and criteria are added to the object using the Python addition operator ``+``, or alternatively the :meth:`_sql.StatementLambdaElement.add_criteria` method which allows for more options.

Lambdaステートメントは :func:`_sql.lambda_stmt` 関数を使用して構築されます。この関数は :class:`_sql.StatementLambdaElement` のインスタンスを返します。これ自体が実行可能なステートメント構造です。追加の修飾子と条件は、Pythonの加算演算子 ``+`` 、またはより多くのオプションを可能にする :meth:`_sql.StatementLambdaElement.add_criteria` メソッドを使用してオブジェクトに追加されます。

.. It is assumed that the :func:`_sql.lambda_stmt` construct is being invoked within an enclosing function or method that expects to be used many times within an application, so that subsequent executions beyond the first one can take advantage of the compiled SQL being cached.  When the lambda is constructed inside of an enclosing function in Python it is then subject to also having closure variables, which are significant to the whole approach::

:func:`_sql.lambda_stmt` 構文は、アプリケーション内で何度も使用されることが予想される包含関数またはメソッド内で呼び出されることを想定しています。そのため、最初の実行以降の後続の実行では、キャッシュされているコンパイル済みSQLを利用できます。Pythonの包含関数内でlambdaが構築されると、ク行ジャー変数も必要になります。これは、アプ行チ全体にとって重要です::

    from sqlalchemy import lambda_stmt


    def run_my_statement(connection, parameter):
        stmt = lambda_stmt(lambda: select(table))
        stmt += lambda s: s.where(table.c.col == parameter)
        stmt += lambda s: s.order_by(table.c.id)

        return connection.execute(stmt)


    with engine.connect() as conn:
        result = run_my_statement(some_connection, "some parameter")

.. Above, the three ``lambda`` callables that are used to define the structure of a SELECT statement are invoked exactly once, and the resulting SQL string cached in the compilation cache of the engine.   From that point forward, the ``run_my_statement()`` function may be invoked any number of times and the ``lambda`` callables within it will not be called, only used as cache keys to retrieve the already-compiled SQL.

上の例では、SELECT文の構造を定義するために使用される3つの ``lambda`` 呼び出し可能オブジェクトは1回だけ呼び出され、結果のSQL文字列はエンジンのコンパイルキャッシュにキャッシュされます。その後、 ``run_my_statement()`` 関数は何度でも呼び出すことができ、その中の ``lambda`` 呼び出し可能オブジェクトは呼び出されず、すでにコンパイルされたSQLを取得するためのキャッシュキーとしてのみ使用されます。

.. .. note::  It is important to note that there is already SQL caching in place when the lambda system is not used.   The lambda system only adds an additional layer of work reduction per SQL statement invoked by caching the building up of the SQL construct itself and also using a simpler cache key.

.. note:: lambdaシステムが使用されていない場合は、すでにSQLキャッシュが配置されていることに注意してください。lambdaシステムは、SQL構文自体の構築をキャッシュし、より単純なキャッシュキーを使用することによって、呼び出されるSQLステートメントごとに作業削減の追加レイヤーを追加するだけです。

Quick Guidelines for Lambdas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Above all, the emphasis within the lambda SQL system is ensuring that there is never a mismatch between the cache key generated for a lambda and the SQL string it will produce.   The :class:`_sql.LambdaElement` and related objects will run and analyze the given lambda in order to calculate how it should be cached on each run, trying to detect any potential problems.  Basic guidelines include:

何よりも、lambda SQLシステム内で強調されているのは、lambdaに対して生成されたキャッシュキーと、それが生成するSQL文字列との間に不一致がないことを保証することです。 :class:`_sql.LambdaElement` および関連するオブジェクトは、指定されたlambdaを実行して分析し、各実行時にどのようにキャッシュされるべきかを計算し、潜在的な問題を検出しようとします。基本的なガイドラインは次のとおりです。

.. * **Any kind of statement is supported** - while it's expected that :func:`_sql.select` constructs are the prime use case for :func:`_sql.lambda_stmt`, DML statements such as :func:`_sql.insert` and :func:`_sql.update` are equally usable::

* **あらゆる種類の文がサポートされています** - :func:`_sql.select` 構文が :func:`_sql.lambda_stmt` の主要なユースケースであることが期待されていますが、 :func:`_sql.insert` や :func:`_sql.update` などのDML文も同じように使用できます::

    def upd(id_, newname):
        stmt = lambda_stmt(lambda: users.update())
        stmt += lambda s: s.values(name=newname)
        stmt += lambda s: s.where(users.c.id == id_)
        return stmt


    with engine.begin() as conn:
        conn.execute(upd(7, "foo"))

  ..

.. * **ORM use cases directly supported as well** - the :func:`_sql.lambda_stmt` can accommodate ORM functionality completely and used directly with :meth:`_orm.Session.execute`::

* **ORMユースケースも直接サポートされています** - :func:`_sql.lambda_stmt` はORM機能に完全に対応でき、 :meth:`_orm.Session.execute` で直接使用されます::

    def select_user(session, name):
        stmt = lambda_stmt(lambda: select(User))
        stmt += lambda s: s.where(User.name == name)

        row = session.execute(stmt).first()
        return row

  ..

.. * **Bound parameters are automatically accommodated** - in contrast to SQLAlchemy's previous "baked query" system, the lambda SQL system accommodates for Python literal values which become SQL bound parameters automatically.  This means that even though a given lambda runs only once, the values that become bound parameters are extracted from the **closure** of the lambda on every run:

* **バウンドパラメータは自動的に調整されます** - SQLAlchemyの以前の"baked query"システムとは対照的に、lambda SQLシステムは自動的にSQLバウンドパラメータになるPythonリテラル値に対応します。これは、特定のlambdaが1回しか実行されない場合でも、バウンドパラメータになる値は実行のたびにlambdaの **ク行ジャー** から抽出されることを意味します。

  .. sourcecode:: pycon+sql

        >>> def my_stmt(x, y):
        ...     stmt = lambda_stmt(lambda: select(func.max(x, y)))
        ...     return stmt
        >>> engine = create_engine("sqlite://", echo=True)
        >>> with engine.connect() as conn:
        ...     print(conn.scalar(my_stmt(5, 10)))
        ...     print(conn.scalar(my_stmt(12, 8)))
        {execsql}SELECT max(?, ?) AS max_1
        [generated in 0.00057s] (5, 10){stop}
        10
        {execsql}SELECT max(?, ?) AS max_1
        [cached since 0.002059s ago] (12, 8){stop}
        12

..   Above, :class:`_sql.StatementLambdaElement` extracted the values of ``x`` and ``y`` from the **closure** of the lambda that is generated each time ``my_stmt()`` is invoked; these were substituted into the cached SQL construct as the values of the parameters.

  上の例では、 :class:`_sql.StatementLambdaElement` は、 ``my_stmt()`` が呼び出されるたびに生成されるlambdaの **ク行ジャー** から ``x`` と ``y`` の値を抽出しています。これらはパラメータの値としてキャッシュされたSQL構文に代入されています。

.. * **The lambda should ideally produce an identical SQL structure in all cases** - Avoid using conditionals or custom callables inside of lambdas that might make it produce different SQL based on inputs; if a function might conditionally use two different SQL fragments, use two separate lambdas::

* **lambdaは理想的には全ての場合で同一のSQL構造を生成するべきです** - 入力に基づいて異なるSQLを生成する可能性のある条件やカスタム呼び出し可能をlambda内で使用することは避けてください;関数が条件付きで2つの異なるSQLフラグメントを使用する可能性がある場合は、2つの別々のlambdaを使用してください::

        # **Don't** do this:


        def my_stmt(parameter, thing=False):
            stmt = lambda_stmt(lambda: select(table))
            stmt += lambda s: (
                s.where(table.c.x > parameter) if thing else s.where(table.c.y == parameter)
            )
            return stmt


        # **Do** do this:


        def my_stmt(parameter, thing=False):
            stmt = lambda_stmt(lambda: select(table))
            if thing:
                stmt += lambda s: s.where(table.c.x > parameter)
            else:
                stmt += lambda s: s.where(table.c.y == parameter)
            return stmt

  .. There are a variety of failures which can occur if the lambda does not produce a consistent SQL construct and some are not trivially detectable right now.

  lambdaが一貫性のあるSQL構文を生成しない場合に発生する可能性のあるさまざまな障害があり、現時点では簡単に検出できないものもあります。

.. * **Don't use functions inside the lambda to produce bound values** - the bound value tracking approach requires that the actual value to be used in the SQL statement be locally present in the closure of the lambda.  This is not possible if values are generated from other functions, and the :class:`_sql.LambdaElement` should normally raise an error if this is attempted::

* **バインド値を生成するためにlambda内の関数を使用しないでください** - バインド値を追跡するアプ行チでは、SQL文で使用される実際の値がlambdaのク行ジャー内に行カルに存在する必要があります。値が他の関数から生成された場合、これは不可能であり、 :class:`_sql.LambdaElement` は通常、これを実行しようとするとエラーを発生します::

    >>> def my_stmt(x, y):
    ...     def get_x():
    ...         return x
    ...
    ...     def get_y():
    ...         return y
    ...
    ...     stmt = lambda_stmt(lambda: select(func.max(get_x(), get_y())))
    ...     return stmt
    >>> with engine.connect() as conn:
    ...     print(conn.scalar(my_stmt(5, 10)))
    Traceback (most recent call last):
      # ...
    sqlalchemy.exc.InvalidRequestError: Can't invoke Python callable get_x()
    inside of lambda expression argument at
    <code object <lambda> at 0x7fed15f350e0, file "<stdin>", line 6>;
    lambda SQL constructs should not invoke functions from closure variables
    to produce literal values since the lambda SQL system normally extracts
    bound values without actually invoking the lambda or any functions within it.

..   Above, the use of ``get_x()`` and ``get_y()``, if they are necessary, should occur **outside** of the lambda and assigned to a local closure variable::

  上記では、必要であれば、 ``get_x()`` と ``get_y()`` の使用は、lambdaの **外側** で行われ、行カルのク行ジャー変数に割り当てられるべきです::

    >>> def my_stmt(x, y):
    ...     def get_x():
    ...         return x
    ...
    ...     def get_y():
    ...         return y
    ...
    ...     x_param, y_param = get_x(), get_y()
    ...     stmt = lambda_stmt(lambda: select(func.max(x_param, y_param)))
    ...     return stmt

  ..

.. * **Avoid referring to non-SQL constructs inside of lambdas as they are not cacheable by default** - this issue refers to how the :class:`_sql.LambdaElement` creates a cache key from other closure variables within the statement.  In order to provide the best guarantee of an accurate cache key, all objects located in the closure of the lambda are considered to be significant, and none will be assumed to be appropriate for a cache key by default.  So the following example will also raise a rather detailed error message::

* **デフォルトではキャッシュ可能ではないため、lambda内の非SQL構成体を参照することは避けてください** - この問題は、 :class:`_sql.LambdaElement` がステートメント内の他のク行ジャー変数からキャッシュキーを作成する方法を参照しています。正確なキャッシュキーの最善の保証を提供するために、lambdaのク行ジャー内にあるすべてのオブジェクトは重要であると見なされ、デフォルトではキャッシュキーに適切であると見なされるものはありません。そのため、次の例でもかなり詳細なエラーメッセージが表示されます::

    >>> class Foo:
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    >>> def my_stmt(foo):
    ...     stmt = lambda_stmt(lambda: select(func.max(foo.x, foo.y)))
    ...     return stmt
    >>> with engine.connect() as conn:
    ...     print(conn.scalar(my_stmt(Foo(5, 10))))
    Traceback (most recent call last):
      # ...
    sqlalchemy.exc.InvalidRequestError: Closure variable named 'foo' inside of
    lambda callable <code object <lambda> at 0x7fed15f35450, file
    "<stdin>", line 2> does not refer to a cacheable SQL element, and also
    does not appear to be serving as a SQL literal bound value based on the
    default SQL expression returned by the function.  This variable needs to
    remain outside the scope of a SQL-generating lambda so that a proper cache
    key may be generated from the lambda's state.  Evaluate this variable
    outside of the lambda, set track_on=[<elements>] to explicitly select
    closure elements to track, or set track_closure_variables=False to exclude
    closure variables from being part of the cache key.

..   The above error indicates that :class:`_sql.LambdaElement` will not assume that the ``Foo`` object passed in will continue to behave the same in all cases.    It also won't assume it can use ``Foo`` as part of the cache key by default; if it were to use the ``Foo`` object as part of the cache key, if there were many different ``Foo`` objects this would fill up the cache with duplicate information, and would also hold long-lasting references to all of these objects.

..   上記のエラーは、 :class:`_sql.LambdaElement` が、渡された ``Foo`` オブジェクトがすべての場合に同じ動作を続けるとは想定していないことを示しています。また、デフォルトでキャッシュキーの一部として ``Foo`` を使用できるとは想定していません。 ``Foo`` オブジェクトをキャッシュキーの一部として使用する場合、多くの異なる ``Foo`` オブジェクトがあると、キャッシュが重複した情報でいっぱいになり、これらのオブジェクトすべてへの長期にわたる参照も保持されます。

  The best way to resolve the above situation is to not refer to ``foo`` inside of the lambda, and refer to it **outside** instead::

  上記の問題を解決する最善の方法は、lambdaの内部ではなく、 **外部** で ``foo`` を参照することです。

    >>> def my_stmt(foo):
    ...     x_param, y_param = foo.x, foo.y
    ...     stmt = lambda_stmt(lambda: select(func.max(x_param, y_param)))
    ...     return stmt

  .. In some situations, if the SQL structure of the lambda is guaranteed to never change based on input, to pass ``track_closure_variables=False`` which will disable any tracking of closure variables other than those used for bound parameters::

  状況によっては、lambdaのSQL構造が入力に基づいて変更されないことが保証されている場合は、 ``track_closure_variables=False`` を渡して、バインドされたパラメータに使用される以外のク行ジャー変数の追跡を無効にします::

    >>> def my_stmt(foo):
    ...     stmt = lambda_stmt(
    ...         lambda: select(func.max(foo.x, foo.y)), track_closure_variables=False
    ...     )
    ...     return stmt

  .. There is also the option to add objects to the element to explicitly form part of the cache key, using the ``track_on`` parameter; using this parameter allows specific values to serve as the cache key and will also prevent other closure variables from being considered.  This is useful for cases where part of the SQL being constructed originates from a contextual object of some sort that may have many different values.  In the example below, the first segment of the SELECT statement will disable tracking of the ``foo`` variable, whereas the second segment will explicitly track ``self`` as part of the cache key::

  また、 ``track_on`` パラメータを使用して、明示的にキャッシュキーの一部を形成するオブジェクトを要素に追加するオプションもあります。このパラメータを使用すると、特定の値がキャッシュキーとして機能し、他のク行ジャー変数が考慮されなくなります。これは、構築されるSQLの一部が、多くの異なる値を持つ可能性のある何らかのコンテキストオブジェクトに由来する場合に便利です。次の例では、SELECT文の最初のセグメントが ``foo`` 変数の追跡を無効にし、2番目のセグメントがキャッシュキーの一部として ``self`` 変数を明示的に追跡します。

    >>> def my_stmt(self, foo):
    ...     stmt = lambda_stmt(
    ...         lambda: select(*self.column_expressions), track_closure_variables=False
    ...     )
    ...     stmt = stmt.add_criteria(lambda: self.where_criteria, track_on=[self])
    ...     return stmt

  .. Using ``track_on`` means the given objects will be stored long term in the lambda's internal cache and will have strong references for as long as the cache doesn't clear out those objects (an LRU scheme of 1000 entries is used by default).

  ``track_on`` を使用することは、指定されたオブジェクトがlambdaの内部キャッシュに長期間保存され、キャッシュがそれらのオブジェクトをクリアしない限り強い参照を持つことを意味します(デフォルトでは1000エントリのLRUスキームが使用されます)。

  ..


Cache Key Generation
^^^^^^^^^^^^^^^^^^^^

.. In order to understand some of the options and behaviors which occur with lambda SQL constructs, an understanding of the caching system is helpful.

lambda SQL構文で発生するいくつかのオプションと動作を理解するには、キャッシュシステムの理解が役立ちます。

.. SQLAlchemy's caching system normally generates a cache key from a given SQL expression construct by producing a structure that represents all the state within the construct::

SQLAlchemyのキャッシュシステムは通常、与えられたSQL式の構成体から、その構成体の中のすべての状態を表す構造体を生成して、キャッシュキーを生成します::

    >>> from sqlalchemy import select, column
    >>> stmt = select(column("q"))
    >>> cache_key = stmt._generate_cache_key()
    >>> print(cache_key)  # somewhat paraphrased
    CacheKey(key=(
      '0',
      <class 'sqlalchemy.sql.selectable.Select'>,
      '_raw_columns',
      (
        (
          '1',
          <class 'sqlalchemy.sql.elements.ColumnClause'>,
          'name',
          'q',
          'type',
          (
            <class 'sqlalchemy.sql.sqltypes.NullType'>,
          ),
        ),
      ),
      # a few more elements are here, and many more for a more
      # complicated SELECT statement
    ),)


.. The above key is stored in the cache which is essentially a dictionary, and the value is a construct that among other things stores the string form of the SQL statement, in this case the phrase "SELECT q".  We can observe that even for an extremely short query the cache key is pretty verbose as it has to represent everything that may vary about what's being rendered and potentially executed.

上記のキーは、本質的には辞書であるキャッシュに格納され、値は、とりわけSQL文の文字列形式(この場合は"SELECT q"というフレーズ)を格納する構造体です。非常に短いクエリであっても、キャッシュキーは、レンダリングされ、実行される可能性のあるものに関して変化する可能性のあるすべてを表現しなければならないため、非常に冗長であることがわかります。

.. The lambda construction system by contrast creates a different kind of cache key::

対照的に、lambda構築システムは別の種類のキャッシュキーを作成します。

    >>> from sqlalchemy import lambda_stmt
    >>> stmt = lambda_stmt(lambda: select(column("q")))
    >>> cache_key = stmt._generate_cache_key()
    >>> print(cache_key)
    CacheKey(key=(
      <code object <lambda> at 0x7fed1617c710, file "<stdin>", line 1>,
      <class 'sqlalchemy.sql.lambdas.StatementLambdaElement'>,
    ),)

.. Above, we see a cache key that is vastly shorter than that of the non-lambda statement, and additionally that production of the ``select(column("q"))`` construct itself was not even necessary; the Python lambda itself contains an attribute called ``__code__`` which refers to a Python code object that within the runtime of the application is immutable and permanent.

上記では、非lambda文のキャッシュキーよりも大幅に短いキャッシュキーが表示されています。さらに、 ``select(column("q"))`` 構文自体の生成は必要ありませんでした。Pythonのlambda自体には、アプリケーションの実行時に不変で永続的なPythonコードオブジェクトを参照する ``__code__`` という属性が含まれています。

.. When the lambda also includes closure variables, in the normal case that these variables refer to SQL constructs such as column objects, they become part of the cache key, or if they refer to literal values that will be bound parameters, they are placed in a separate element of the cache key::

lambdaにク行ジャー変数も含まれている場合、これらの変数が列オブジェクトなどのSQL構成体を参照する通常のケースでは、これらはキャッシュキーの一部になります。また、バインドされるパラメータとなるリテラル値を参照する場合は、キャッシュキーの別の要素に配置されます::

    >>> def my_stmt(parameter):
    ...     col = column("q")
    ...     stmt = lambda_stmt(lambda: select(col))
    ...     stmt += lambda s: s.where(col == parameter)
    ...     return stmt

.. The above :class:`_sql.StatementLambdaElement` includes two lambdas, both of which refer to the ``col`` closure variable, so the cache key will represent both of these segments as well as the ``column()`` object::

上の :class:`_sql.StatementLambdaElement` には2つのlambdaが含まれていて、どちらもク行ジャー変数の ``col`` を参照しているので、キャッシュキーはこれらのセグメントと ``column()`` オブジェクトの両方を表します::

    >>> stmt = my_stmt(5)
    >>> key = stmt._generate_cache_key()
    >>> print(key)
    CacheKey(key=(
      <code object <lambda> at 0x7f07323c50e0, file "<stdin>", line 3>,
      (
        '0',
        <class 'sqlalchemy.sql.elements.ColumnClause'>,
        'name',
        'q',
        'type',
        (
          <class 'sqlalchemy.sql.sqltypes.NullType'>,
        ),
      ),
      <code object <lambda> at 0x7f07323c5190, file "<stdin>", line 4>,
      <class 'sqlalchemy.sql.lambdas.LinkedLambdaElement'>,
      (
        '0',
        <class 'sqlalchemy.sql.elements.ColumnClause'>,
        'name',
        'q',
        'type',
        (
          <class 'sqlalchemy.sql.sqltypes.NullType'>,
        ),
      ),
      (
        '0',
        <class 'sqlalchemy.sql.elements.ColumnClause'>,
        'name',
        'q',
        'type',
        (
          <class 'sqlalchemy.sql.sqltypes.NullType'>,
        ),
      ),
    ),)


.. The second part of the cache key has retrieved the bound parameters that will be used when the statement is invoked::

キャッシュキーの2番目の部分は、文が呼び出されたときに使用されるバウンドパラメータを取得しています。

    >>> key.bindparams
    [BindParameter('%(139668884281280 parameter)s', 5, type_=Integer())]


.. For a series of examples of "lambda" caching with performance comparisons, see the "short_selects" test suite within the :ref:`examples_performance` performance example.

"lambda" キャッシングとパフォーマンス比較の一連の例については、 :ref:`examples_performance` パフォーマンス例内の"short_selects"テストスイートを参照してください。

.. _engine_insertmanyvalues:

"Insert Many Values" Behavior for INSERT statements
---------------------------------------------------

.. .. versionadded:: 2.0 see :ref:`change_6047` for background on the change including sample performance tests

.. versionadded:: 2.0 サンプルパフォーマンステストを含む変更の背景については :ref:`change_6047` を参照してください

.. .. tip:: The :term:`insertmanyvalues` feature is a **transparently available** performance feature which requires no end-user intervention in order for it to take place as needed. This section describes the architecture of the feature as well as how to measure its performance and tune its behavior in order to optimize the speed of bulk INSERT statements, particularly as used by the ORM.

.. tip:: :term:`insertmanyvalues` 機能は、必要に応じて実行するためにエンドユーザの介入を必要としない、 **透過的に利用可能な** パフォーマンス機能です。このセクションでは、この機能のアーキテクチャと、特にORMで使用されるバルクインサートステートメントの速度を最適化するために、パフォーマンスを測定し、動作を調整する方法について説明します。

.. As more databases have added support for INSERT..RETURNING, SQLAlchemy has undergone a major change in how it approaches the subject of INSERT statements where there's a need to acquire server-generated values, most importantly server-generated primary key values which allow the new row to be referenced in subsequent operations. In particular, this scenario has long been a significant performance issue in the ORM, which relies on being able to retrieve server-generated primary key values in order to correctly populate the :term:`identity map`.

より多くのデータベースがINSERT..RETURNINGのサポートを追加するにつれて、SQLAlchemyは、サーバが生成した値を取得する必要があるINSERT文の主題へのアプ行チにおいて大きな変化を経験しました。最も重要なのは、新しい行を後続の操作で参照できるようにするサーバが生成したプライマリ・キー値です。特に、このシナリオは、 :term:`identity map` を正しく生成するためにサーバが生成したプライマリ・キー値を取得できることに依存しているORMでは、長い間大きなパフォーマンスの問題でした。

.. With recent support for RETURNING added to SQLite and MariaDB, SQLAlchemy no longer needs to rely upon the single-row-only `cursor.lastrowid <https://peps.python.org/pep-0249/#lastrowid>`_ attribute provided by the :term:`DBAPI` for most backends; RETURNING may now be used for all :ref:`SQLAlchemy-included <included_dialects>` backends with the exception of MySQL. The remaining performance limitation, that the `cursor.executemany() <https://peps.python.org/pep-0249/#executemany>`_ DBAPI method does not allow for rows to be fetched, is resolved for most backends by foregoing the use of ``executemany()`` and instead restructuring individual INSERT statements to each accommodate a large number of rows in a single statement that is invoked using ``cursor.execute()``. This approach originates from the `psycopg2 fast execution helpers <https://www.psycopg.org/docs/extras.html#fast-execution-helpers>`_ feature of the ``psycopg2`` DBAPI, which SQLAlchemy incrementally added more and more support towards in recent release series.

SQLiteとMariaDBに最近追加されたRETURNINGのサポートにより、SQLAlchemyは、ほとんどのバックエンドで :term:`DBAPI` によって提供される単一行のみの `cursor.lastrowid <https://peps.python.org/pep-0249/#lastrowid>`_ 属性に依存する必要がなくなりました。RETURNINGは、MySQLを除くすべての :ref:`SQLAlchemy-included<included_dialects>` バックエンドで使用できるようになりました。 `cursor.executemany() <https://peps.python.org/pep-0249/#executemany>`_ DBAPIメソッドが行のフェッチを許可しないという残りのパフォーマンス制限は、ほとんどのバックエンドで解決されます。これは、 ``executemany()`` の使用をやめ、代わりに個々のINSERT文を再構築して、それぞれが ``cursor.execute()`` を使用して呼び出される1つの文に多数の行を収容するようにすることで解決されます。このアプ行チは、SQLAlchemyが最近のリリースシリーズで徐々にサポートを追加した、 ``psycopg2`` DBAPIの `psycopg2 fast execution helpers <https://www.psycopg.org/docs/extras.html#fast-execution-helpers>`_ 機能に由来しています。


Current Support
~~~~~~~~~~~~~~~

.. The feature is enabled for all backend included in SQLAlchemy that support RETURNING, with the exception of Oracle for which both the cx_Oracle and OracleDB drivers offer their own equivalent feature. The feature normally takes place when making use of the :meth:`_dml.Insert.returning` method of an :class:`_dml.Insert` construct in conjunction with :term:`executemany` execution, which occurs when passing a list of dictionaries to the :paramref:`_engine.Connection.execute.parameters` parameter of the :meth:`_engine.Connection.execute` or :meth:`_orm.Session.execute` methods (as well as equivalent methods under :ref:`asyncio <asyncio_toplevel>` and shorthand methods like :meth:`_orm.Session.scalars`). It also takes place within the ORM :term:`unit of work` process when using methods such as :meth:`_orm.Session.add` and :meth:`_orm.Session.add_all` to add rows.

この機能は、RETURNINGをサポートするSQLAlchemyに含まれるすべてのバックエンドで有効になります。ただし、cx_OracleドライバとOracleDBドライバの両方が独自の同等機能を提供しているOracleの場合は例外です。この機能は通常、 :class:`_dml.Insert `構文の :meth:`_dml.Insert.returning` メソッドを :term:`executemany` 実行と組み合わせて使用するときに行われます。この実行は、辞書のリストを :meth:`_engine.Connection.execute` または :meth:`_orm.Session.execute` メソッドの :paramref:`_engine.Connection.execute.parameters` パラメータに渡すときに行われます( :ref:`asyncio<asyncio_toplevel>` の同等のメソッドや :meth:`_orm.Session.scalars` のようなショートハンドメソッドも同様です)。また、ORM :term:`unit of work` プロセス内で、 :meth:`_orm.Session.add`や:meth:`_orm.Session.add_all` などのメソッドを使用して行を追加するときにも行われます。

.. For SQLAlchemy's included dialects, support or equivalent support is currently as follows:

SQLAlchemyに含まれるダイアレクトのサポートまたは同等のサポートは、現在次のとおりです:

.. * SQLite - supported for SQLite versions 3.35 and above
.. * PostgreSQL - all supported Postgresql versions (9 and above)
.. * SQL Server - all supported SQL Server versions [#]_
.. * MariaDB - supported for MariaDB versions 10.5 and above
.. * MySQL - no support, no RETURNING feature is present
.. * Oracle - supports RETURNING with executemany using native cx_Oracle / OracleDB APIs, for all supported Oracle versions 9 and above, using multi-row OUT parameters. This is not the same implementation as "executemanyvalues", however has the same usage patterns and equivalent performance benefits.

* SQLite - SQLiteバージョン3.35以上でサポートされます。
* PostgreSQL - サポートされているすべてのPostgreSQLバージョン(9以降)
* SQL Server-  サポートされているすべてのSQL Serverバージョン[#]_
* MariaDB - MariaDBバージョン10.5以上でサポート
* MySQL - サポートされていません。RETURNING機能はありません。
* Oracle - サポートされているすべてのOracleバージョン9以上で、複数行のOUTパラメータを使用して、ネイティブcx_Oracle/OracleDB APIを使用したexecutemanyでのRETURNINGをサポートします。これは"executemanyvalues"と同じ実装ではありませんが、同じ使用パターンと同等のパフォーマンス上の利点があります。

.. versionchanged:: 2.0.10

   .. .. [#] "insertmanyvalues" support for Microsoft SQL Server is restored, after being temporarily disabled in version 2.0.9.

   .. [#] Microsoft SQL Serverの"insertmanyvalues"サポートは、バージョン2.0.9で一時的に無効にされた後、復元されました。

Disabling the feature
~~~~~~~~~~~~~~~~~~~~~

.. To disable the "insertmanyvalues" feature for a given backend for an :class:`.Engine` overall, pass the :paramref:`_sa.create_engine.use_insertmanyvalues` parameter as ``False`` to :func:`_sa.create_engine`::

:class:`.Engine` 全体で、指定されたバックエンドの"insertmanyvalues"機能を無効にするには、 :paramref:`_sa.create_engine.use_insertmanyvalues` パラメータを ``False`` として :func:`_sa.create_engine` に渡します::

    engine = create_engine(
        "mariadb+mariadbconnector://scott:tiger@host/db", use_insertmanyvalues=False
    )

.. The feature can also be disabled from being used implicitly for a particular :class:`_schema.Table` object by passing the :paramref:`_schema.Table.implicit_returning` parameter as ``False``::

:paramref:`_schema.Table.implicit_returning` パラメータを ``False`` として渡すことで、この機能が特定の :class:`_schema.Table` オブジェクトに対して暗黙的に使用されないようにすることもできます::

      t = Table(
          "t",
          metadata,
          Column("id", Integer, primary_key=True),
          Column("x", Integer),
          implicit_returning=False,
      )

.. The reason one might want to disable RETURNING for a specific table is to work around backend-specific limitations.

特定のテーブルに対してRETURNINGを無効にしたい理由は、バックエンド固有の制限を回避するためです。


Batched Mode Operation
~~~~~~~~~~~~~~~~~~~~~~

.. The feature has two modes of operation, which are selected transparently on a per-dialect, per-:class:`_schema.Table` basis. One is **batched mode**, which reduces the number of database round trips by rewriting an INSERT statement of the form:

この機能には2つの操作モードがあり、方言ごと、 :class:`_schema.Table` ごとに透過的に選択されます。1つは **バッチモード** で、次の形式のINSERT文を書き換えることで、データベースのラウンドトリップ回数を減らします:

.. sourcecode:: sql

    INSERT INTO a (data, x, y) VALUES (%(data)s, %(x)s, %(y)s) RETURNING a.id

.. into a "batched" form such as:

次のような"バッチ"形式に変換します:

.. sourcecode:: sql

    INSERT INTO a (data, x, y) VALUES
        (%(data_0)s, %(x_0)s, %(y_0)s),
        (%(data_1)s, %(x_1)s, %(y_1)s),
        (%(data_2)s, %(x_2)s, %(y_2)s),
        ...
        (%(data_78)s, %(x_78)s, %(y_78)s)
    RETURNING a.id

.. where above, the statement is organized against a subset (a "batch") of the input data, the size of which is determined by the database backend as well as the number of parameters in each batch to correspond to known limits for statement size / number of parameters.  The feature then executes the INSERT statement once for each batch of input data until all records are consumed, concatenating the RETURNING results for each batch into a single large rowset that's available from a single :class:`_result.Result` object.

上記の場合、文は入力データのサブセット("バッチ")に対して編成され、そのサイズはデータベースバックエンドによって決定されます。また、各バッチ内のパラメータの数は、文のサイズ/パラメータ数の既知の制限に対応します。次に、この機能は、すべてのレコードが消費されるまで、入力データの各バッチに対して1回INSERT文を実行し、各バッチのRETURNING結果を、単一の :class:`_result.Result` オブジェクトから利用可能な単一の大きな行セットに連結します。

.. This "batched" form allows INSERT of many rows using much fewer database round trips, and has been shown to allow dramatic performance improvements for most backends where it's supported.

この"バッチ"形式を使用すると、より少ないデータベース・ラウンドトリップで多数の行のINSERTが可能になり、サポートされているほとんどのバックエンドでパフォーマンスが大幅に向上することが示されています。

.. _engine_insertmanyvalues_returning_order:

Correlating RETURNING rows to parameter sets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.0.10

.. The "batch" mode query illustrated in the previous section does not guarantee the order of records returned would correspond with that of the input data.  When used by the SQLAlchemy ORM :term:`unit of work` process, as well as for applications which correlate returned server-generated values with input data, the :meth:`_dml.Insert.returning` and :meth:`_dml.UpdateBase.return_defaults` methods include an option :paramref:`_dml.Insert.returning.sort_by_parameter_order` which indicates that "insertmanyvalues" mode should guarantee this correspondence. This is **not related** to the order in which records are actually INSERTed by the database backend, which is **not** assumed under any circumstances; only that the returned records should be organized when received back to correspond to the order in which the original input data was passed.

前のセクションで説明した"バッチ"モードのクエリは、返されるレコードの順序が入力データの順序と一致することを保証しません。SQLAlchemy ORM :term:`unit of work` プロセスや、返されたサーバ生成の値を入力データと関連付けるアプリケーションで使用される場合、 :meth:`_dml.Insert.returning` および :meth:`_dml.UpdateBase.return_defaults` メソッドには、オプション :paramref:`_dml.Insert.returning.sort_by_parameter_order` が含まれます。これは、"insertmanyvalues"モードがこの対応を保証することを示します。これは、データベースバックエンドによって実際にレコードが挿入される順序とは **関係ありません** 。これは、いかなる状況においても **想定されていません** 。返されたレコードは、元の入力データが渡された順序に対応するように、受信時に整理される必要があるだけです。

.. When the :paramref:`_dml.Insert.returning.sort_by_parameter_order` parameter is present, for tables that use server-generated integer primary key values such as ``IDENTITY``, PostgreSQL ``SERIAL``, MariaDB ``AUTO_INCREMENT``, or SQLite's ``ROWID`` scheme, "batch" mode may instead opt to use a more complex INSERT..RETURNING form, in conjunction with post-execution sorting of rows based on the returned values, or if such a form is not available, the "insertmanyvalues" feature may gracefully degrade to "non-batched" mode which runs individual INSERT statements for each parameter set.

:paramref:`_dml.Insert.returning.sort_by_parameter_order` パラメータが存在する場合、サーバが生成した整数のプライマリキー値を使用するテーブル(例えば、 ``IDENTITY`` 、PostgreSQLの ``SERIAL`` 、MariaDBの ``AUTO_INCREMENT`` 、SQLiteの ``ROWID`` スキームなど)では、"バッチ"モードは、より複雑なINSERT.RETURNING形式を、戻り値に基づく実行後の行のソートと組み合わせて使用することを選択するか、そのような形式が利用できない場合、"insertmanyvalues"機能は、各パラメータセットに対して個々のINSERT文を実行する"非バッチ"モードに優雅に劣化する可能性があります。

.. For example, on SQL Server when an auto incrementing ``IDENTITY`` column is used as the primary key, the following SQL form is used:

例えば、SQL Serverでは、自動的にインクリメントされる ``IDENTITY`` 列がプライマリキーとして使用される場合、次のSQL形式が使用されます。

.. sourcecode:: sql

    INSERT INTO a (data, x, y)
    OUTPUT inserted.id, inserted.id AS id__1
    SELECT p0, p1, p2 FROM (VALUES
        (?, ?, ?, 0), (?, ?, ?, 1), (?, ?, ?, 2),
        ...
        (?, ?, ?, 77)
    ) AS imp_sen(p0, p1, p2, sen_counter) ORDER BY sen_counter

.. A similar form is used for PostgreSQL as well, when primary key columns use SERIAL or IDENTITY. The above form **does not** guarantee the order in which rows are inserted. However, it does guarantee that the IDENTITY or SERIAL values will be created in order with each parameter set [#]_. The "insertmanyvalues" feature then sorts the returned rows for the above INSERT statement by incrementing integer identity.

同様の形式は、主キー列がSERIALまたはIDENTITYを使用する場合にPostgreSQLでも使用されます。上記の形式は、 **行が挿入される順序を保証しません** 。ただし、IDENTITYまたはSERIALの値が各パラメータセット [#]_ の順序で作成されることは保証します。"insertmanyvalues"機能は、上記のINSERT文に対して返された行を、整数IDENTITYを増分することによってソートします。

.. For the SQLite database, there is no appropriate INSERT form that can correlate the production of new ROWID values with the order in which the parameter sets are passed.  As a result, when using server-generated primary key values, the SQLite backend will degrade to "non-batched" mode when ordered RETURNING is requested.  For MariaDB, the default INSERT form used by insertmanyvalues is sufficient, as this database backend will line up the order of AUTO_INCREMENT with the order of input data when using InnoDB [#]_.

SQLiteデータベースの場合、新しいROWID値の生成とパラメータセットが渡される順序を関連付けることができる適切なINSERTフォームはありません。その結果、サーバー生成の主キー値を使用する場合、SQLiteバックエンドは、順序付きRETURNINGが要求されると「非バッチ」モードに低下します。MariaDBの場合、insertmanyvaluesで使用されるデフォルトのINSERTフォームで十分です。これは、InnoDB [#]_ を使用する場合、このデータベースバックエンドはAUTO_INCREMENTの順序と入力データの順序を一致させるためです。

.. For a client-side generated primary key, such as when using the Python ``uuid.uuid4()`` function to generate new values for a :class:`.Uuid` column, the "insertmanyvalues" feature transparently includes this column in the RETURNING records and correlates its value to that of the given input records, thus maintaining correspondence between input records and result rows. From this, it follows that all backends allow for batched, parameter-correlated RETURNING order when client-side-generated primary key values are used.

Pythonの ``uuid.uuid4()`` 関数を使用して :class:`.Uuid` 列の新しい値を生成する場合のように、クライアント側で生成された主キーの場合、"insertmanyvalues"機能はこの列をRETURNINGレコードに透過的に含め、その値を指定された入力レコードの値と相関させます。これにより、入力レコードと結果行の間の対応が維持されます。このことから、クライアント側で生成された主キー値が使用される場合、すべてのバックエンドでは、バッチ化されたパラメータ相関のあるRETURNING順序が可能になることがわかります。

.. The subject of how "insertmanyvalues" "batch" mode determines a column or columns to use as a point of correspondence between input parameters and RETURNING rows is known as an :term:`insert sentinel`, which is a specific column or columns that are used to track such values. The "insert sentinel" is normally selected automatically, however can also be user-configuration for extremely special cases; the section :ref:`engine_insertmanyvalues_sentinel_columns` describes this.

"insertmanyvalues" "batch"モードが、入力パラメータとRETURNING行との対応点として使用する1つ以上の列をどのように決定するかという問題は、 :term:`insert sentinel` として知られています。これは、そのような値を追跡するために使用される特定の1つ以上の列です。"insert sentinel"は通常自動的に選択されますが、非常に特殊な場合にはユーザが設定することもできます。 :ref:`engine_insertmanyvalues_sentinel_columns` で説明されています。

.. For backends that do not offer an appropriate INSERT form that can deliver server-generated values deterministically aligned with input values, or for :class:`_schema.Table` configurations that feature other kinds of server generated primary key values, "insertmanyvalues" mode will make use of **non-batched** mode when guaranteed RETURNING ordering is requested.

入力値と決定論的に一致したサーバ生成値を提供できる適切なINSERT形式を提供しないバックエンドや、他の種類のサーバ生成主キー値を特徴とする :class:`_schema.Table` 構成では、保証されたRETURNING順序が要求された場合、"insertmanyvalues"モードは **non-batched** モードを使用します。

.. seealso::

    .. [#]

    .. * Microsoft SQL Server rationale

    * Microsoft SQL Serverの理論的根拠

      .. "INSERT queries that use SELECT with ORDER BY to populate rows guarantees how identity values are computed but not the order in which the rows are inserted." https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16#limitations-and-restrictions

      "SELECTとORDER BYを使用して行を生成するINSERTクエリでは、ID値の計算方法は保証されますが、行の挿入順序は保証されません。"https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16#limitations-and-restrictions

    * PostgreSQL batched INSERT Discussion

      .. Original description in 2018 https://www.postgresql.org/message-id/29386.1528813619@sss.pgh.pa.us

      2018年の最初の記述 https://www.postgresql.org/message-id/29386.1528813619@sss.pgh.pa.us

      .. Follow up in 2023 - https://www.postgresql.org/message-id/be108555-da2a-4abc-a46b-acbe8b55bd25%40app.fastmail.com

      2023年のフォローアップ - https://www.postgresql.org/message-id/be108555-da2a-4abc-a46b-acbe8b55bd25%40app.fastmail.com

    .. [#]

    .. * MariaDB AUTO_INCREMENT behavior (using the same InnoDB engine as MySQL):

    * MariaDB AUTO_INCREMENTの動作(MySQLと同じInnoDBエンジンを使用):

      https://dev.mysql.com/doc/refman/8.0/en/innodb-auto-increment-handling.html

      https://dba.stackexchange.com/a/72099

.. _engine_insertmanyvalues_non_batch:

Non-Batched Mode Operation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. For :class:`_schema.Table` configurations that do not have client side primary key values, and offer server-generated primary key values (or no primary key) that the database in question is not able to invoke in a deterministic or sortable way relative to multiple parameter sets, the "insertmanyvalues" feature when tasked with satisfying the :paramref:`_dml.Insert.returning.sort_by_parameter_order` requirement for an :class:`_dml.Insert` statement may instead opt to use **non-batched mode**.

クライアント側のプライマリキー値を持たず、サーバが生成したプライマリキー値を提供する(あるいはプライマリキーを持たない) :class:`_schema.Table` 構成で、問題のデータベースが複数のパラメータセットに対して決定性やソート性のある方法で呼び出すことができない場合、 :class:`_dml.Insert` 文の :paramref:`_dml.Insert.returning.sort_by_parameter_order` 要件を満たすための"insertmanyvalues"機能は、代わりに **非バッチモード** を使用することを選択できます。

.. In this mode, the original SQL form of INSERT is maintained, and the "insertmanyvalues" feature will instead run the statement as given for each parameter set individually, organizing the returned rows into a full result set. Unlike previous SQLAlchemy versions, it does so in a tight loop that minimizes Python overhead. In some cases, such as on SQLite, "non-batched" mode performs exactly as well as "batched" mode.

このモードでは、INSERTの元のSQL形式が維持され、代わりに「insertmanyvalues」機能によって、各パラメータセットに対して指定されたとおりにステートメントが個別に実行され、返された行が完全な結果セットに編成されます。以前のSQLAlchemyバージョンとは異なり、Pythonのオーバーヘッドを最小限に抑えるタイトなループで実行されます。SQLiteなどの場合、 "非バッチ"モードは"バッチ"モードとまったく同じように実行されます。

Statement Execution Model
~~~~~~~~~~~~~~~~~~~~~~~~~

.. For both "batched" and "non-batched" modes, the feature will necessarily invoke **multiple INSERT statements** using the DBAPI ``cursor.execute()`` method, within the scope of  **single** call to the Core-level :meth:`_engine.Connection.execute` method, with each statement containing up to a fixed limit of parameter sets.  This limit is configurable as described below at :ref:`engine_insertmanyvalues_page_size`.  The separate calls to ``cursor.execute()`` are logged individually and also individually passed along to event listeners such as :meth:`.ConnectionEvents.before_cursor_execute` (see :ref:`engine_insertmanyvalues_events` below).

"バッチ"モードと"非バッチ"モードの両方で、この機能は、コアレベルの :meth:`_engine.Connection.execute` メソッドへの**単一**呼び出しの範囲内で、DBAPIの ``cursor.execute()`` メソッドを使用して、 **複数のINSERT文** を呼び出す必要があります。各ステートメントには、パラメータセットの固定された制限が含まれます。この制限は、以下の :ref:`engine_insertmanyvalues_page_size` で説明するように設定できます。 ``cursor.execute()`` への個別の呼び出しは個別にログに記録され、 :meth:`.ConnectionEvents.before_cursor_execute` などのイベントリスナにも個別に渡されます(下記の :ref:`engine_insertmanyvalues_events` を参照)。

.. _engine_insertmanyvalues_sentinel_columns:

Configuring Sentinel Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. In typical cases, the "insertmanyvalues" feature in order to provide INSERT..RETURNING with deterministic row order will automatically determine a sentinel column from a given table's primary key, gracefully degrading to "row at a time" mode if one cannot be identified. As a completely **optional** feature, to get full "insertmanyvalues" bulk performance for tables that have server generated primary keys whose default generator functions aren't compatible with the "sentinel" use case, other non-primary key columns may be marked as "sentinel" columns assuming they meet certain requirements. A typical example is a non-primary key :class:`_sqltypes.Uuid` column with a client side default such as the Python ``uuid.uuid4()`` function.  There is also a construct to create simple integer columns with a a client side integer counter oriented towards the "insertmanyvalues" use case.

典型的なケースでは、確定的な行順序でINSERT.RETURNINGを提供するための"insertmanyvalues"機能は、指定されたテーブルの主キーから自動的にセンチネル列を決定し、識別できない場合は"row at a time"モードに優雅に劣化します。完全に **オプション** の機能として、デフォルトの生成関数が"センチネル"ユースケースと互換性のないサーバ生成主キーを持つテーブルの完全な"insertmanyvalues"バルクパフォーマンスを得るために、他の非主キー列は、特定の要件を満たすことを前提として"センチネル"列としてマークされることがあります。典型的な例は、Pythonの ``uuid.uuid4()`` 関数のようなクライアント側のデフォルトを持つ非主キー :class:`_sqltypes.Uuid` 列です。また、"insertmanyvalues"ユースケース向けのクライアント側の整数カウンタを持つ単純な整数列を作成する構成体もあります。

.. Sentinel columns may be indicated by adding :paramref:`_schema.Column.insert_sentinel` to qualifying columns.   The most basic "qualifying" column is a not-nullable, unique column with a client side default, such as a UUID column as follows::

Sentinel列は、 :paramref:`_schema.Column.insert_sentinel` を修飾列に追加することで示すことができます。最も基本的な"修飾"列は、次のようなUUID列のような、クライアント側のデフォルトを持つNULL不可の一意の列です::

    import uuid

    from sqlalchemy import Column
    from sqlalchemy import FetchedValue
    from sqlalchemy import Integer
    from sqlalchemy import String
    from sqlalchemy import Table
    from sqlalchemy import Uuid

    my_table = Table(
        "some_table",
        metadata,
        # assume some arbitrary server-side function generates
        # primary key values, so cannot be tracked by a bulk insert
        Column("id", String(50), server_default=FetchedValue(), primary_key=True),
        Column("data", String(50)),
        Column(
            "uniqueid",
            Uuid(),
            default=uuid.uuid4,
            nullable=False,
            unique=True,
            insert_sentinel=True,
        ),
    )

.. When using ORM Declarative models, the same forms are available using the :class:`_orm.mapped_column` construct::

ORM宣言モデルを使用する場合、 :class:`_orm.mapped_column` 構文を使用して同じ形式を使用できます::

    import uuid

    from sqlalchemy.orm import DeclarativeBase
    from sqlalchemy.orm import Mapped
    from sqlalchemy.orm import mapped_column


    class Base(DeclarativeBase):
        pass


    class MyClass(Base):
        __tablename__ = "my_table"

        id: Mapped[str] = mapped_column(primary_key=True, server_default=FetchedValue())
        data: Mapped[str] = mapped_column(String(50))
        uniqueid: Mapped[uuid.UUID] = mapped_column(
            default=uuid.uuid4, unique=True, insert_sentinel=True
        )

.. While the values generated by the default generator **must** be unique, the actual UNIQUE constraint on the above "sentinel" column, indicated by the ``unique=True`` parameter, itself is optional and may be omitted if not desired.

デフォルトジェネレータが生成する値は **一意でなければなりません** が、上記の"sentinel"列に対する実際のUNIQUE制約は、 ``unique=True`` パラメータで示されますが、それ自体はオプションであり、必要でなければ省略することができます。

.. There is also a special form of "insert sentinel" that's a dedicated nullable integer column which makes use of a special default integer counter that's only used during "insertmanyvalues" operations; as an additional behavior, the column will omit itself from SQL statements and result sets and behave in a mostly transparent manner.  It does need to be physically present within the actual database table, however.  This style of :class:`_schema.Column` may be constructed using the function :func:`_schema.insert_sentinel`::

また、"insert sentinel"という特別な形式もあります。これは、"insertmanyvalues"操作中にのみ使用される特別なデフォルトの整数カウンタを利用する、NULL許容整数列です。追加の動作として、列はSQL文と結果セットから自身を省略し、ほとんど透過的に動作します。ただし、実際のデータベーステーブル内に物理的に存在する必要があります。このスタイルの :class:`_schema.Column` は、関数 :func:`_schema.insert_sentinel` を使用して構築できます::

    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import String
    from sqlalchemy import Table
    from sqlalchemy import Uuid
    from sqlalchemy import insert_sentinel

    Table(
        "some_table",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("data", String(50)),
        insert_sentinel("sentinel"),
    )

.. When using ORM Declarative, a Declarative-friendly version of :func:`_schema.insert_sentinel` is available called :func:`_orm.orm_insert_sentinel`, which has the ability to be used on the Base class or a mixin; if packaged using :func:`_orm.declared_attr`, the column will apply itself to all table-bound subclasses including within joined inheritance hierarchies::

ORM宣言型を使用する場合、宣言型に対応したバージョンの :func:`_schema.insert_sentinel` が利用できます。これは :func:`_orm.orm_insert_sentinel` と呼ばれ、Baseクラスまたはmixinで使用できます。 :func:`_orm.declared_attr` を使用してパッケージ化された場合、列は結合された継承階層内を含むすべてのテーブルバウンドサブクラスに適用されます::

    from sqlalchemy.orm import declared_attr
    from sqlalchemy.orm import DeclarativeBase
    from sqlalchemy.orm import Mapped
    from sqlalchemy.orm import mapped_column
    from sqlalchemy.orm import orm_insert_sentinel


    class Base(DeclarativeBase):
        @declared_attr
        def _sentinel(cls) -> Mapped[int]:
            return orm_insert_sentinel()


    class MyClass(Base):
        __tablename__ = "my_table"

        id: Mapped[str] = mapped_column(primary_key=True, server_default=FetchedValue())
        data: Mapped[str] = mapped_column(String(50))


    class MySubClass(MyClass):
        __tablename__ = "sub_table"

        id: Mapped[str] = mapped_column(ForeignKey("my_table.id"), primary_key=True)


    class MySingleInhClass(MyClass):
        pass

.. In the example above, both "my_table" and "sub_table" will have an additional integer column named "_sentinel" that can be used by the "insertmanyvalues" feature to help optimize bulk inserts used by the ORM.

上記の例では、"my_table"と"sub_table"の両方に"_sentinel"という名前の整数列が追加されます。この列は、ORMで使用されるバルク挿入を最適化するために"insertmanyvalues"機能で使用できます。

.. _engine_insertmanyvalues_page_size:

Controlling the Batch Size
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. A key characteristic of "insertmanyvalues" is that the size of the INSERT statement is limited on a fixed max number of "values" clauses as well as a dialect-specific fixed total number of bound parameters that may be represented in one INSERT statement at a time. When the number of parameter dictionaries given exceeds a fixed limit, or when the total number of bound parameters to be rendered in a single INSERT statement exceeds a fixed limit (the two fixed limits are separate), multiple INSERT statements will be invoked within the scope of a single :meth:`_engine.Connection.execute` call, each of which accommodate for a portion of the parameter dictionaries, known as a "batch".  The number of parameter dictionaries represented within each "batch" is then known as the "batch size".  For example, a batch size of 500 means that each INSERT statement emitted will INSERT at most 500 rows.

"insertmanyvalues"の重要な特徴は、INSERT文のサイズが"values"句の固定された最大数と、一度に1つのINSERT文で表現できるバウンドパラメータの方言固有の固定された合計数に制限されていることです。与えられたパラメータ辞書の数が固定された制限を超えた場合、または単一のINSERT文でレンダリングされるバウンドパラメータの合計数が固定された制限を超えた場合(2つの固定された制限は別々です)、単一の :meth:`_engine.Connection.execute` 呼び出しのスコープ内で複数のINSERT文が呼び出されます。それぞれの呼び出しは、"バッチ"と呼ばれるパラメータ辞書の一部を収容します。各"バッチ"内で表現されるパラメータ辞書の数は、"バッチサイズ"と呼ばれます。たとえば、バッチサイズが500の場合、生成される各INSERT文は最大500行をINSERTします。

.. It's potentially important to be able to adjust the batch size, as a larger batch size may be more performant for an INSERT where the value sets themselves are relatively small, and a smaller batch size may be more appropriate for an INSERT that uses very large value sets, where both the size of the rendered SQL as well as the total data size being passed in one statement may benefit from being limited to a certain size based on backend behavior and memory constraints.  For this reason the batch size can be configured on a per-:class:`.Engine` as well as a per-statement basis.   The parameter limit on the other hand is fixed based on the known characteristics of the database in use.

バッチサイズを調整できることが重要になる可能性があります。なぜなら、値セット自体が比較的小さいINSERTでは、バッチサイズを大きくする方がパフォーマンスが高くなる可能性があります。また、非常に大きい値セットを使用するINSERTでは、バッチサイズを小さくする方が適切である可能性があります。非常に大きい値セットを使用するINSERTでは、レンダリングされるSQLのサイズと1つの文で渡されるデータの合計サイズの両方が、バックエンドの動作とメモリの制約に基づいて特定のサイズに制限されることでメリットが得られる可能性があります。このため、バッチサイズは、文ごとだけでなく、 :class:`.Engine` ごとにも設定できます。一方、パラメータの制限は、使用中のデータベースの既知の特性に基づいて固定されます。

.. The batch size defaults to 1000 for most backends, with an additional per-dialect "max number of parameters" limiting factor that may reduce the batch size further on a per-statement basis. The max number of parameters varies by dialect and server version; the largest size is 32700 (chosen as a healthy distance away from PostgreSQL's limit of 32767 and SQLite's modern limit of 32766, while leaving room for additional parameters in the statement as well as for DBAPI quirkiness). Older versions of SQLite (prior to 3.32.0) will set this value to 999. MariaDB has no established limit however 32700 remains as a limiting factor for SQL message size.

バッチサイズのデフォルトは、ほとんどのバックエンドで1000であり、追加の方言ごとの"パラメータの最大数"制限要因により、ステートメントごとにバッチサイズがさらに削減される可能性があります。パラメータの最大数は、方言とサーバのバージョンによって異なります。最大サイズは32700です(PostgreSQLの制限である32767とSQLiteの最新の制限である32766からの適切な距離として選択されますが、ステートメント内の追加パラメータとDBAPIの奇抜さのための余地が残されています)。SQLiteの古いバージョン(3.32.0より前)では、この値は999に設定されます。MariaDBには確立された制限はありませんが、32700はSQLメッセージサイズの制限要因として残っています。

.. The value of the "batch size" can be affected :class:`_engine.Engine` wide via the :paramref:`_sa.create_engine.insertmanyvalues_page_size` parameter.  Such as, to affect INSERT statements to include up to 100 parameter sets in each statement::

"バッチサイズ"の値は、 :paramref:`_sa.create_engine.insertmanyvalues_page_size` パラメータを介して :class:`_engine.Engine` の広さに影響を与えることができます。たとえば、INSERT文に影響を与えて、各文に最大100個のパラメータセットを含めるには::

    e = create_engine("sqlite://", insertmanyvalues_page_size=100)

.. The batch size may also be affected on a per statement basis using the :paramref:`_engine.Connection.execution_options.insertmanyvalues_page_size` execution option, such as per execution::

バッチサイズは、実行ごとに :paramref:`_engine.Connection.execution_options.insertmanyvalues_page_size` 実行オプションを使用して、文ごとに影響を受けることもあります。たとえば、次のようになります::

    with e.begin() as conn:
        result = conn.execute(
            table.insert().returning(table.c.id),
            parameterlist,
            execution_options={"insertmanyvalues_page_size": 100},
        )

.. Or configured on the statement itself::

または、文自体で設定します::

    stmt = (
        table.insert()
        .returning(table.c.id)
        .execution_options(insertmanyvalues_page_size=100)
    )
    with e.begin() as conn:
        result = conn.execute(stmt, parameterlist)

.. _engine_insertmanyvalues_events:

Logging and Events
~~~~~~~~~~~~~~~~~~

.. The "insertmanyvalues" feature integrates fully with SQLAlchemy's :ref:`statement logging <dbengine_logging>` as well as cursor events such as :meth:`.ConnectionEvents.before_cursor_execute`.  When the list of parameters is broken into separate batches, **each INSERT statement is logged and passed to event handlers individually**.   This is a major change compared to how the psycopg2-only feature worked in previous 1.x series of SQLAlchemy, where the production of multiple INSERT statements was hidden from logging and events.  Logging display will truncate the long lists of parameters for readability, and will also indicate the specific batch of each statement. The example below illustrates an excerpt of this logging:

"insertmanyvalues"機能は、SQLAlchemyの :ref:`statement logging <dbengine_logging>` や、 :meth:`.ConnectionEvents.before_cursor_execute` などのカーソルイベントと完全に統合されます。パラメータのリストが別々のバッチに分割されている場合、 **各INSERT文は個別にログに記録され、イベントハンドラに渡されます** 。これは、複数のINSERT文の生成がログとイベントから隠されていた以前の1.xシリーズのSQLAlchemyでのpsycopg2のみの機能と比較して大きな変更です。ログ表示では、読みやすくするためにパラメータの長いリストが切り捨てられ、各文の特定のバッチも示されます。次の例は、このログの抜粋を示しています。

.. sourcecode:: text

  INSERT INTO a (data, x, y) VALUES (?, ?, ?), ... 795 characters truncated ...  (?, ?, ?), (?, ?, ?) RETURNING id
  [generated in 0.00177s (insertmanyvalues) 1/10 (unordered)] ('d0', 0, 0, 'd1',  ...
  INSERT INTO a (data, x, y) VALUES (?, ?, ?), ... 795 characters truncated ...  (?, ?, ?), (?, ?, ?) RETURNING id
  [insertmanyvalues 2/10 (unordered)] ('d100', 100, 1000, 'd101', ...

  ...

  INSERT INTO a (data, x, y) VALUES (?, ?, ?), ... 795 characters truncated ...  (?, ?, ?), (?, ?, ?) RETURNING id
  [insertmanyvalues 10/10 (unordered)] ('d900', 900, 9000, 'd901', ...

.. When :ref:`non-batch mode <engine_insertmanyvalues_non_batch>` takes place, logging will indicate this along with the insertmanyvalues message:

:ref:`non-batch mode <engine_insertmanyvalues_non_batch>` が実行されると、ログはinsertmanyvaluesメッセージとともにこれを示します。

.. sourcecode:: text

  ...

  INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
  [insertmanyvalues 67/78 (ordered; batch not supported)] ('d66', 66, 66)
  INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
  [insertmanyvalues 68/78 (ordered; batch not supported)] ('d67', 67, 67)
  INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
  [insertmanyvalues 69/78 (ordered; batch not supported)] ('d68', 68, 68)
  INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
  [insertmanyvalues 70/78 (ordered; batch not supported)] ('d69', 69, 69)

  ...

.. seealso::

    :ref:`dbengine_logging`

Upsert Support
~~~~~~~~~~~~~~

.. The PostgreSQL, SQLite, and MariaDB dialects offer backend-specific "upsert" constructs :func:`_postgresql.insert`, :func:`_sqlite.insert` and :func:`_mysql.insert`, which are each :class:`_dml.Insert` constructs that have an additional method such as ``on_conflict_do_update()` or ``on_duplicate_key()``.   These constructs also support "insertmanyvalues" behaviors when they are used with RETURNING, allowing efficient upserts with RETURNING to take place.

PostgreSQL、SQLite、MariaDBダイアレクトでは、バックエンド固有の"upsert"構文として :func:`_PostgreSQL.insert` 、 :func:`_SQLite.insert` 、 :func:`_mysql.insert` が提供されています。これらはそれぞれ :class:`_dml.Insert` 構文で、 ``on_conflict_do_update()`` や ``on_duplicate_key()`` などのメソッドが追加されています。これらの構文は、RETURNINGとともに使用された場合の"insertmanyvalues"動作もサポートしており、RETURNINGによる効率的なupsertが可能になっています。

.. _engine_disposal:

Engine Disposal
---------------

.. The :class:`_engine.Engine` refers to a connection pool, which means under normal circumstances, there are open database connections present while the :class:`_engine.Engine` object is still resident in memory.   When an :class:`_engine.Engine` is garbage collected, its connection pool is no longer referred to by that :class:`_engine.Engine`, and assuming none of its connections are still checked out, the pool and its connections will also be garbage collected, which has the effect of closing out the actual database connections as well.   But otherwise, the :class:`_engine.Engine` will hold onto open database connections assuming it uses the normally default pool implementation of :class:`.QueuePool`.

:class:`_engine.Engine` は接続プールを参照します。これは、通常の状況では、 :class:`_engine.Engine` オブジェクトがまだメモリに存在している間は、開いているデータベース接続が存在することを意味します。 :class:`_engine.Engine` がガベージコレクションされると、その接続プールはその :class:`_engine.Engine` によって参照されなくなり、その接続がまだチェックアウトされていないと仮定すると、プールとその接続もガベージコレクションされ、実際のデータベース接続も閉じられます。しかし、そうでなければ、 :class:`_engine.Engine` は、通常はデフォルトのプール実装である :class:`.QueuePool` を使用すると仮定して、開いているデータベース接続を保持します。

.. The :class:`_engine.Engine` is intended to normally be a permanent fixture established up-front and maintained throughout the lifespan of an application.  It is **not** intended to be created and disposed on a per-connection basis; it is instead a registry that maintains both a pool of connections as well as configurational information about the database and DBAPI in use, as well as some degree of internal caching of per-database resources.

:class:`_engine.Engine` は、通常、前もって確立され、アプリケーションの寿命を通じて維持される永続的なフィクスチャであることが意図されています。これは、接続ごとに作成され、配置されることを意図したものでは **ありません** 。代わりに、接続のプールと、使用中のデータベースとDBAPIに関する構成情報、およびデータベースごとのリソースのある程度の内部キャッシュの両方を維持するレジストリです。

.. However, there are many cases where it is desirable that all connection resources referred to by the :class:`_engine.Engine` be completely closed out.  It's generally not a good idea to rely on Python garbage collection for this to occur for these cases; instead, the :class:`_engine.Engine` can be explicitly disposed using the :meth:`_engine.Engine.dispose` method.   This disposes of the engine's underlying connection pool and replaces it with a new one that's empty.  Provided that the :class:`_engine.Engine` is discarded at this point and no longer used, all **checked-in** connections which it refers to will also be fully closed.

しかし、多くの場合、 :class:`_engine.Engine` が参照するすべての接続リソースが完全に閉じられることが望まれます。一般的に、このような場合にPythonのガベージコレクションに頼るのは良い考えではありません。代わりに、 :class:`_engine.Engine` は :meth:`_engine.Engine.dispose` メソッドを使って明示的に破棄することができます。これにより、エンジンの基礎となる接続プールが破棄され、空の新しい接続プールに置き換えられます。 :class:`_engine.Engine` がこの時点で破棄されて使用されなくなれば、それが参照するすべての **チェックインされた** 接続も完全に閉じられます。

.. Valid use cases for calling :meth:`_engine.Engine.dispose` include:

:meth:`_engine.Engine.dispose` を呼び出す有効なユースケースは次のとおりです:

.. * When a program wants to release any remaining checked-in connections held by the connection pool and expects to no longer be connected to that database at all for any future operations.

* プログラムが、接続プールによって保持されている残りのチェックインされた接続を解放し、将来の操作のためにそのデータベースに接続されなくなることを予期している場合。

.. * When a program uses multiprocessing or ``fork()``, and an :class:`_engine.Engine` object is copied to the child process, :meth:`_engine.Engine.dispose` should be called so that the engine creates brand new database connections local to that fork.   Database connections generally do **not** travel across process boundaries.  Use the :paramref:`.Engine.dispose.close` parameter set to False in this case.  See the section :ref:`pooling_multiprocessing` for more background on this use case.

* プログラムがマルチプロセッシングまたは ``fork()`` を使用し、 :class:`_engine.Engine` オブジェクトが子プロセスにコピーされる場合、 :meth:`_engine.Engine.dispose` を呼び出して、エンジンがそのフォークに対してローカルな新しいデータベース接続を作成するようにします。データベース接続は通常、プロセスの境界を越えて移動 **しません** 。この場合は、 :paramref:`.Engine.dispose.close` パラメータをFalseに設定して使用します。この使用例の背景については :ref:`pooling_multiprocessing` の節を参照してください。

.. * Within test suites or multitenancy scenarios where many ad-hoc, short-lived :class:`_engine.Engine` objects may be created and disposed.

* テストスイートまたはマルチテナンシのシナリオで、多くのアドホックで短命な :class:`_engine.Engine` オブジェクトが作成され、破棄される可能性がある場合。

.. Connections that are **checked out** are **not** discarded when the engine is disposed or garbage collected, as these connections are still strongly referenced elsewhere by the application.  However, after :meth:`_engine.Engine.dispose` is called, those connections are no longer associated with that :class:`_engine.Engine`; when they are closed, they will be returned to their now-orphaned connection pool which will ultimately be garbage collected, once all connections which refer to it are also no longer referenced anywhere.  Since this process is not easy to control, it is strongly recommended that :meth:`_engine.Engine.dispose` is called only after all checked out connections are checked in or otherwise de-associated from their pool.

**チェックアウトされた** 接続は、エンジンが破棄またはガベージコレクションされても **破棄されません** 。なぜなら、これらの接続はアプリケーションによって他の場所で強く参照されているからです。ただし、 :meth:`_engine.Engine.dispose` が呼び出された後、これらの接続はその :class:`_engine.Engine` に関連付けられなくなります。これらの接続が閉じられると、現在は切り離された接続プールに戻されます。この接続プールは、それを参照するすべての接続も参照されなくなると、最終的にガベージコレクションされます。このプロセスを制御するのは簡単ではないので、 :meth:`_engine.Engine.dispose` は、チェックアウトされたすべての接続がチェックインされた後、またはその他の方法で接続プールから関連付けが解除された後にのみ呼び出すことを強くお勧めします。

.. An alternative for applications that are negatively impacted by the :class:`_engine.Engine` object's use of connection pooling is to disable pooling entirely.  This typically incurs only a modest performance impact upon the use of new connections, and means that when a connection is checked in, it is entirely closed out and is not held in memory.  See :ref:`pool_switching` for guidelines on how to disable pooling.

:class:`_engine.Engine` オブジェクトが接続プーリングを使用することによって悪影響を受けるアプリケーションのための代替手段は、プーリングを完全に無効にすることです。これは通常、新しい接続を使用する際に性能にわずかな影響を与えるだけで、接続がチェックインされたときに完全に閉じられ、メモリに保持されないことを意味します。プーリングを無効にする方法のガイドラインについては :ref:`pool_switching` を参照してください。

.. seealso::

    :ref:`pooling_toplevel`

    :ref:`pooling_multiprocessing`

.. _dbapi_connections:

Working with Driver SQL and Raw DBAPI Connections
-------------------------------------------------

.. The introduction on using :meth:`_engine.Connection.execute` made use of the :func:`_expression.text` construct in order to illustrate how textual SQL statements may be invoked.  When working with SQLAlchemy, textual SQL is actually more of the exception rather than the norm, as the Core expression language and the ORM both abstract away the textual representation of SQL.  However, the :func:`_expression.text` construct itself also provides some abstraction of textual SQL in that it normalizes how bound parameters are passed, as well as that it supports datatyping behavior for parameters and result set rows.

:meth:`_engine.Connection.execute` の使用法の紹介では、 :func:`_expression.text` 構文を使用して、テキストSQL文がどのように呼び出されるかを説明しています。SQLAlchemyを使用する場合、Core式言語とORMの両方がSQLのテキスト表現を抽象化しているため、テキストSQLは実際には標準ではなく例外です。ただし、 :func:`_expression.text` 構文自体も、バインドされたパラメータがどのように渡されるかを標準化し、パラメータと結果セット行のデータ型付け動作をサポートするという点で、テキストSQLの抽象化を提供します。

Invoking SQL strings directly to the driver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. For the use case where one wants to invoke textual SQL directly passed to the underlying driver (known as the :term:`DBAPI`) without any intervention from the :func:`_expression.text` construct, the :meth:`_engine.Connection.exec_driver_sql` method may be used::

:func:`_expression.text` 構文を使わずに、ドライバ( :term:`DBAPI` と呼ばれます)に直接渡されるテキストSQLを呼び出したい場合には、 :meth:`_engine.Connection.exec_driver_sql` メソッドを使うことができます::

    with engine.connect() as conn:
        conn.exec_driver_sql("SET param='bar'")

.. .. versionadded:: 1.4  Added the :meth:`_engine.Connection.exec_driver_sql` method.

.. versionadded:: 1.4 :meth:`_engine.Connection.exec_driver_sql` メソッドを追加しました。

.. _dbapi_connections_cursor:

Working with the DBAPI cursor directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. There are some cases where SQLAlchemy does not provide a genericized way at accessing some :term:`DBAPI` functions, such as calling stored procedures as well as dealing with multiple result sets.  In these cases, it's just as expedient to deal with the raw DBAPI connection directly.

SQLAlchemyでは、ストアドプロシージャの呼び出しや複数の結果セットの処理など、いくつかの :term:`DBAPI` 関数への汎用的なアクセス方法が提供されない場合があります。このような場合は、生のDBAPI接続を直接処理するのも同様に便利です。

.. The most common way to access the raw DBAPI connection is to get it from an already present :class:`_engine.Connection` object directly.  It is present using the :attr:`_engine.Connection.connection` attribute::

生のDBAPI接続にアクセスする最も一般的な方法は、既に存在する :class:`_engine.Connection` オブジェクトから直接取得することです。これは :attr:`_engine.Connection.connection` 属性を使用して存在します::

    connection = engine.connect()
    dbapi_conn = connection.connection

.. The DBAPI connection here is actually a "proxied" in terms of the originating connection pool, however this is an implementation detail that in most cases can be ignored.    As this DBAPI connection is still contained within the scope of an owning :class:`_engine.Connection` object, it is best to make use of the :class:`_engine.Connection` object for most features such as transaction control as well as calling the :meth:`_engine.Connection.close` method; if these operations are performed on the DBAPI connection directly, the owning :class:`_engine.Connection` will not be aware of these changes in state.

ここでのDBAPI接続は、実際には元の接続プールに関して"プロキシ"されていますが、これはほとんどの場合無視できる実装の詳細です。このDBAPI接続はまだ所有する :class:`_engine.Connection` オブジェクトのスコープ内に含まれているので、トランザクション制御や :meth:`_engine.Connection.close` メソッドの呼び出しなど、ほとんどの機能で :class:`_engine.Connection` オブジェクトを利用するのが最善です。これらの操作がDBAPI接続で直接実行される場合、所有する :class:`_engine.Connection` はこれらの状態の変化を認識しません。

.. To overcome the limitations imposed by the DBAPI connection that is maintained by an owning :class:`_engine.Connection`, a DBAPI connection is also available without the need to procure a :class:`_engine.Connection` first, using the :meth:`_engine.Engine.raw_connection` method of :class:`_engine.Engine`::

所有する :class:`_engine.Connection` によって維持されるDBAPI接続によって課される制限を克服するために、最初に :class:`_engine.Connection` を調達しなくても、 :class:`_engine.Engine` の :meth:`_engine.Engine.raw_connection` メソッドを使用してDBAPI接続を利用することもできます::

    dbapi_conn = engine.raw_connection()

.. This DBAPI connection is again a "proxied" form as was the case before.  The purpose of this proxying is now apparent, as when we call the ``.close()`` method of this connection, the DBAPI connection is typically not actually closed, but instead :term:`released` back to the engine's connection pool::

このDBAPI接続は、以前の場合と同様に"プロキシ"された形式です。このプロキシの目的は明らかです。この接続の ``.close()`` メソッドを呼び出すと、DBAPI接続は通常実際には閉じられず、代わりにエンジンの接続プールに :term:`released` されます::

    dbapi_conn.close()

.. While SQLAlchemy may in the future add built-in patterns for more DBAPI use cases, there are diminishing returns as these cases tend to be rarely needed and they also vary highly dependent on the type of DBAPI in use, so in any case the direct DBAPI calling pattern is always there for those cases where it is needed.

SQLAlchemyは将来、より多くのDBAPIユースケースに対して組み込みパターンを追加する可能性がありますが、これらのケースはほとんど必要とされない傾向があり、使用するDBAPIのタイプに大きく依存するため、収益は減少しています。したがって、いずれにしても、直接DBAPI呼び出しパターンは、必要とされるケースに対して常に存在します。

.. seealso::

    :ref:`faq_dbapi_connection` - includes additional details about how
    the DBAPI connection is accessed as well as the "driver" connection
    when using asyncio drivers.

.. Some recipes for DBAPI connection use follow.

DBAPI接続を使用するためのいくつかのレシピを次に示します。

.. _stored_procedures:

Calling Stored Procedures and User Defined Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. SQLAlchemy supports calling stored procedures and user defined functions several ways. Please note that all DBAPIs have different practices, so you must consult your underlying DBAPI's documentation for specifics in relation to your particular usage. The following examples are hypothetical and may not work with your underlying DBAPI.

SQLAlchemyでは、複数の方法でストアド・プロシージャおよびユーザー定義関数を呼び出すことができます。すべてのDBAPIには異なる方法があるため、特定の使用方法に関する詳細については、基礎となるDBAPIのドキュメントを参照する必要があります。次の例は仮定のものであり、基礎となるDBAPIでは機能しない場合があります。

.. For stored procedures or functions with special syntactical or parameter concerns, DBAPI-level `callproc <https://legacy.python.org/dev/peps/pep-0249/#callproc>`_ may potentially be used with your DBAPI. An example of this pattern is::

特別な構文やパラメータに関係するストアドプロシージャや関数では、DBAPIレベルの `callproc <https://legacy.python.org/dev/peps/pep-0249/#callproc>`_ がDBAPIで使用される可能性があります。このパターンの例を次に示します::

    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.callproc("my_procedure", ["x", "y", "z"])
        results = list(cursor_obj.fetchall())
        cursor_obj.close()
        connection.commit()
    finally:
        connection.close()

.. note::

    .. Not all DBAPIs use `callproc` and overall usage details will vary. The above example is only an illustration of how it might look to use a particular DBAPI function.

    すべてのDBAPIが `callproc` を使用しているわけではなく、全体的な使用方法の詳細も異なります。上の例は、特定のDBAPI関数を使用した場合の外観を示したものにすぎません。

.. Your DBAPI may not have a ``callproc`` requirement *or* may require a stored procedure or user defined function to be invoked with another pattern, such as normal SQLAlchemy connection usage. One example of this usage pattern is, *at the time of this documentation's writing*, executing a stored procedure in the PostgreSQL database with the psycopg2 DBAPI, which should be invoked with normal connection usage::

DBAPIに ``callproc`` 要件がない場合 *または* ストアドプロシージャまたはユーザ定義関数を、通常のSQLAlchemy接続の使用する場合、別のパターンで呼び出す必要がある場合があります。この使用パターンの例の1つは、*このドキュメントの執筆時点で*、PostgreSQLデータベース内のストアドプロシージャをpsycopg2 DBAPIで実行することです。これは通常の接続で呼び出す必要があります::

    connection.execute("CALL my_procedure();")

.. This above example is hypothetical. The underlying database is not guaranteed to support "CALL" or "SELECT" in these situations, and the keyword may vary dependent on the function being a stored procedure or a user defined function.  You should consult your underlying DBAPI and database documentation in these situations to determine the correct syntax and patterns to use.

前述の例は仮定のものです。基礎となるデータベースでは、このような状況での"CALL"または"SELECT"のサポートが保証されていません。また、キーワードは、ストアド・プロシージャまたはユーザー定義関数である関数によって異なる場合があります。このような状況で正しい構文およびパターンを判断するには、基礎となるDBAPIおよびデータベースのドキュメントを参照してください。

Multiple Result Sets
~~~~~~~~~~~~~~~~~~~~

.. Multiple result set support is available from a raw DBAPI cursor using the `nextset <https://legacy.python.org/dev/peps/pep-0249/#nextset>`_ method::

複数の結果セットのサポートは、 `nextset <https://legacy.python.org/dev/peps/pep-0249/#nextset>`_ メソッドを使用して、生のDBAPIカーソルから利用できます::

    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.execute("select * from table1; select * from table2")
        results_one = cursor_obj.fetchall()
        cursor_obj.nextset()
        results_two = cursor_obj.fetchall()
        cursor_obj.close()
    finally:
        connection.close()

Registering New Dialects
------------------------

.. The :func:`_sa.create_engine` function call locates the given dialect using setuptools entrypoints.   These entry points can be established for third party dialects within the setup.py script.  For example, to create a new dialect "foodialect://", the steps are as follows:

:func:`_sa.create_engine` 関数呼び出しは、setuptoolsのエントリポイントを使用して与えられた方言を見つけます。これらのエントリポイントは、setup.pyスクリプト内でサードパーティの方言に対して確立できます。たとえば、新しい方言"foodialect://""を作成するには、次の手順を実行します。

.. 1. Create a package called ``foodialect``.
.. 2. The package should have a module containing the dialect class, which is typically a subclass of :class:`sqlalchemy.engine.default.DefaultDialect`.  In this example let's say it's called ``FooDialect`` and its module is accessed via ``foodialect.dialect``.
.. 3. The entry point can be established in ``setup.cfg`` as follows:

1. ``foodialect`` というパッケージを作成します。
2. パッケージには、ダイアレクトクラスを含むモジュールが必要です。これは通常、 :class:`sqlalchemy.engine.default.DefaultDialect` のサブクラスです。この例では、それが ``FooDialect`` と呼ばれ、そのモジュールが「FooDialect.dialect」を介してアクセスされるとします。
3. エントリポイントは、次のようにして ``setup.cfg`` に設定できます。

   .. sourcecode:: ini

          [options.entry_points]
          sqlalchemy.dialects =
              foodialect = foodialect.dialect:FooDialect

.. If the dialect is providing support for a particular DBAPI on top of an existing SQLAlchemy-supported database, the name can be given including a database-qualification.  For example, if ``FooDialect`` were in fact a MySQL dialect, the entry point could be established like this:

既存のSQLAlchemyでサポートされているデータベースに加えて、特定のDBAPIをサポートしているダイアレクトの場合は、データベース修飾を含めて名前を指定できます。例えば、 ``FooDialect`` が実際にMySQLダイアレクトである場合、エントリポイントは次のように設定できます:



.. sourcecode:: ini

      [options.entry_points]
      sqlalchemy.dialects
          mysql.foodialect = foodialect.dialect:FooDialect

.. The above entrypoint would then be accessed as ``create_engine("mysql+foodialect://")``.

上記のエントリポイントは ``create_engine("mysql+foodialect://")`` としてアクセスされます。


Registering Dialects In-Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. SQLAlchemy also allows a dialect to be registered within the current process, bypassing the need for separate installation.   Use the ``register()`` function as follows::

また、SQLAlchemyを使用すると、現在のプロセス内にダイアレクトを登録できるため、個別にインストールする必要がありません。次のように ``register()`` 関数を使用してください::

    from sqlalchemy.dialects import registry


    registry.register("mysql.foodialect", "myapp.dialect", "MyMySQLDialect")

.. The above will respond to ``create_engine("mysql+foodialect://")`` and load the ``MyMySQLDialect`` class from the ``myapp.dialect`` module.

上記は ``create_engine("mysql+foodialect://")`` に応答して、 ``myapp.dialect`` モジュールから ``MyMySQLDialect`` クラスをロードします。


Connection / Engine API
-----------------------

.. autoclass:: Connection
   :members:

.. autoclass:: CreateEnginePlugin
   :members:

.. autoclass:: Engine
   :members:

.. autoclass:: ExceptionContext
   :members:

.. autoclass:: NestedTransaction
    :members:
    :inherited-members:

.. autoclass:: RootTransaction
    :members:
    :inherited-members:

.. autoclass:: Transaction
    :members:

.. autoclass:: TwoPhaseTransaction
    :members:
    :inherited-members:


Result Set API
---------------

.. autoclass:: ChunkedIteratorResult
    :members:

.. autoclass:: CursorResult
    :members:
    :inherited-members:

.. autoclass:: FilterResult
    :members:

.. autoclass:: FrozenResult
    :members:

.. autoclass:: IteratorResult
    :members:

.. autoclass:: MergedResult
    :members:

.. autoclass:: Result
    :members:
    :inherited-members:

.. autoclass:: ScalarResult
    :members:
    :inherited-members:

.. autoclass:: MappingResult
    :members:
    :inherited-members:

.. autoclass:: Row
    :members:
    :private-members: _asdict, _fields, _mapping, _t, _tuple

.. autoclass:: RowMapping
    :members:

.. autoclass:: TupleResult
