:orphan:

.. _glossary:

========
Glossary
========

.. glossary::
    :sorted:

    1.x style
    2.0 style
    1.x-style
    2.0-style
        .. These terms are new in SQLAlchemy 1.4 and refer to the SQLAlchemy 1.4-> 2.0 transition plan, described at :ref:`migration_20_toplevel`.  The term "1.x style" refers to an API used in the way it's been documented throughout the 1.x series of SQLAlchemy and earlier (e.g. 1.3, 1.2, etc) and the term "2.0 style" refers to the way an API will look in version 2.0.   Version 1.4 implements nearly all of 2.0's API in so-called "transition mode", while version 2.0 still maintains the legacy :class:`_orm.Query` object to allow legacy code to remain largely 2.0 compatible.

        これらの用語はSQLAlchemy 1.4で新しく追加されたもので、 :ref:`migration_20_toplevel` で説明されているSQLAlchemy 1.4 -> 2.0の移行計画を参照しています。"1.x style"という用語は、SQLAlchemyの1.xシリーズおよびそれ以前(例えば1.3、1.2など)で文書化されている方法で使用されるAPIを指し、"2.0 style"という用語は、バージョン2.0でのAPIの表示方法を指します。バージョン1.4は2.0のAPIのほぼすべてをいわゆる"移行モード"で実装していますが、バージョン2.0はレガシーコードが2.0との互換性を維持できるようにレガシーの:class`_orm.Query`オブジェクトを維持しています。

        .. seealso::

            :ref:`migration_20_toplevel`

    sentinel
    insert sentinel
        .. This is a SQLAlchemy-specific term that refers to a :class:`_schema.Column` which can be used for a bulk         :term:`insertmanyvalues` operation to track INSERTed data records against rows passed back using RETURNING or similar.   Such a column configuration is necessary for those cases when the :term:`insertmanyvalues` feature does an optimized INSERT..RETURNING statement for many rows at once while still being able to guarantee the order of returned rows matches the input data.

        これはSQLAlchemy特有の用語で、 :class`_schema.Column` を参照します。これはバルクの :term:`insertmanyvalues` 操作で使用でき、RETURNINGなどを使用して返された行に対して挿入されたデータレコードを追跡します。このような列設定は、 :term:`insertmanyvalues` 機能が一度に多くの行に対して最適化されたINSERT.RETURNING文を実行し、返された行の順序が入力データと一致することを保証できる場合に必要です。

        .. For typical use cases, the SQLAlchemy SQL compiler can automatically make use of surrogate integer primary key columns as "insert sentinels", and no user-configuration is required. For less common cases with other varieties of server-generated primary key values, explicit "insert sentinel" columns may be optionally configured within :term:`table metadata` in order to optimize INSERT statements that are inserting many rows at once.

        典型的なユースケースでは、SQLAlchemy SQLコンパイラは自動的に"insert sentinel"としてサロゲート整数のプライマリキー列を使用することができ、ユーザによる設定は必要ありません。他の種類のサーバ生成プライマリキー値を使用するあまり一般的でないケースでは、一度に多くの行を挿入するINSERT文を最適化するために、 :term:`table metadata` 内で明示的な"insert sentinel"列をオプションで設定できます。

        .. seealso::

            :ref:`engine_insertmanyvalues_returning_order` - in the section
            :ref:`engine_insertmanyvalues`

    insertmanyvalues
        .. This refers to a SQLAlchemy-specific feature which allows INSERT statements to emit thousands of new rows within a single statement while at the same time allowing server generated values to be returned inline from the statement using RETURNING or similar, for performance optimization purposes. The feature is intended to be transparently available for selected backends, but does offer some configurational options. See the section :ref:`engine_insertmanyvalues` for a full description of this feature.

        これはSQLAlchemy特有の機能で、INSERT文が1つの文の中で何千もの新しい行を出力できるようにすると同時に、パフォーマンスを最適化する目的で、サーバが生成した値をRETURNINGなどを使用して文からインラインで返すことができます。この機能は、選択されたバックエンドで透過的に使用できるように意図されていますが、いくつかの設定オプションを提供します。この機能の詳細な説明については :ref:`engine_insertmanyvalues` を参照してください。


        .. seealso::

            :ref:`engine_insertmanyvalues`

    mixin class
    mixin classes

    ..   A common object-oriented pattern where a class that contains methods or attributes for use by other classes without having to be the parent class of those other classes.

    他のクラスによって使用されるメソッドまたは属性を含むクラスが、それらの他のクラスの親クラスである必要がない、共通のオブジェクト指向パターン。


      .. seealso::

          `Mixin (via Wikipedia) <https://en.wikipedia.org/wiki/Mixin>`_


    reflection
    reflected
        .. In SQLAlchemy, this term refers to the feature of querying a database's schema catalogs in order to load information about existing tables, columns, constraints, and other constructs.   SQLAlchemy includes features that can both provide raw data for this information, as well as that it can construct Core/ORM usable :class:`.Table` objects from database schema catalogs automatically.

        SQLAlchemyでは、この用語は、既存のテーブル、列、制約、およびその他の構成体に関する情報をロードするために、データベースのスキーマカタログを照会する機能を指します。SQLAlchemyには、この情報の生データを提供する機能と、データベーススキーマカタログからCore/ORMで使用可能な :class:`.Table` オブジェクトを自動的に構築する機能の両方が含まれています。


        .. seealso::

            .. :ref:`metadata_reflection_toplevel` - complete background on database reflection.

            :ref:`metadata_reflection_toplevel` - データベースリフレクションのバックグラウンドです。

            .. :ref:`orm_declarative_reflected` - background on integrating ORM mappings with reflected tables.

            :ref:`orm_declarative_reflected` - ORMマッピングとリフレクトされたテーブルの統合に関するバックグラウンドです。


    imperative
    declarative

        .. In the SQLAlchemy ORM, these terms refer to two different styles of mapping Python classes to database tables.

        SQLAlchemy ORMでは、これらの用語はPythonクラスをデータベース・テーブルにマッピングする2つの異なるスタイルを指します。


        .. seealso::

            :ref:`orm_declarative_mapping`

            :ref:`orm_imperative_mapping`

    facade

        .. an object that serves as a front-facing interface masking more complex underlying or structural code.

        より複雑な基礎または構造コードをマスクする、前面のインタフェースとして機能するオブジェクト。

        .. seealso::

            `Facade pattern (via Wikipedia) <https://en.wikipedia.org/wiki/Facade_pattern>`_

    relational
    relational algebra

        .. An algebraic system developed by Edgar F. Codd that is used for modelling and querying the data stored in relational databases.

        リレーショナル・データベースに格納されたデータのモデリングとクエリーに使用される、エドガー・F・コッドによって開発された代数的システム。

        .. seealso::

            `Relational Algebra (via Wikipedia) <https://en.wikipedia.org/wiki/Relational_algebra>`_

    cartesian product

        .. Given two sets A and B, the cartesian product is the set of all ordered pairs (a, b) where a is in A and b is in B.

        2つの集合AとBが与えられた場合、直積はすべての順序付けられた対(a, b)の集合であり、aはAにあり、bはBにあります。

        .. In terms of SQL databases, a cartesian product occurs when we select from two or more tables (or other subqueries) without establishing any kind of criteria between the rows of one table to another (directly or indirectly).  If we SELECT from table A and table B at the same time, we get every row of A matched to the first row of B, then every row of A matched to the second row of B, and so on until every row from A has been paired with every row of B.

        SQLデータベースに関して言えば、直積は、2つ以上のテーブル(またはその他のサブクエリ)から、あるテーブルのローと別のテーブルのローとの間に(直接的または間接的に)何の種類の基準も確立せずに選択する場合に発生します。テーブルAとテーブルBから同時にSELECTを実行すると、AのすべてのローがBの最初のローに一致し、AのすべてのローがBの2番目のローに一致し、AのすべてのローがBのすべてのローとペアになるまで続きます。

        .. Cartesian products cause enormous result sets to be generated and can easily crash a client application if not prevented.

        デカルト積は膨大な結果セットを生成し、防止しなければクライアント・アプリケーションを簡単にクラッシュさせる可能性があります。

        .. seealso::

            `Cartesian Product (via Wikipedia) <https://en.wikipedia.org/wiki/Cartesian_product>`_

    cyclomatic complexity
        .. A measure of code complexity based on the number of possible paths through a program's source code.

        プログラムのソースコード内の可能なパスの数に基づくコードの複雑さの尺度。

        .. seealso::

            `Cyclomatic Complexity <https://en.wikipedia.org/wiki/Cyclomatic_complexity>`_

    bound parameter
    bound parameters
    bind parameter
    bind parameters

        .. Bound parameters are the primary means in which data is passed to the :term:`DBAPI` database driver.    While the operation to be invoked is based on the SQL statement string, the data values themselves are passed separately, where the driver contains logic that will safely process these strings and pass them to the backend database server, which may either involve formatting the parameters into the SQL string itself, or passing them to the database using separate protocols.

        バウンドパラメータは、データが :term:`DBAPI` データベースドライバに渡される主要な手段です。呼び出される操作はSQL文の文字列に基づいていますが、データ値自体は別々に渡されます。ドライバには、これらの文字列を安全に処理してバックエンドのデータベースサーバに渡すロジックが含まれています。これには、パラメータをSQL文字列自体にフォーマットするか、別のプロトコルを使用してデータベースに渡す必要があります。


        .. The specific system by which the database driver does this should not matter to the caller; the point is that on the outside, data should **always** be passed separately and not as part of the SQL string itself.  This is integral both to having adequate security against SQL injections as well as allowing the driver to have the best performance.

        データベースドライバがこれを行う特定のシステムは、呼び出し元には関係ありません。重要なのは、外部では、データはSQL文字列自体の一部としてではなく、**常に**別々に渡されるべきであるということです。これは、SQLインジェクションに対して適切なセキュリティを確保するためにも、ドライバが最高のパフォーマンスを発揮できるようにするためにも不可欠です。


        .. seealso::

            `Prepared Statement <https://en.wikipedia.org/wiki/Prepared_statement>`_ - at Wikipedia

            `bind parameters <https://use-the-index-luke.com/sql/where-clause/bind-parameters>`_ - at Use The Index, Luke!

            :ref:`tutorial_sending_parameters` - in the :ref:`unified_tutorial`

    selectable
        .. A term used in SQLAlchemy to describe a SQL construct that represents a collection of rows.   It's largely similar to the concept of a "relation" in :term:`relational algebra`.  In SQLAlchemy, objects that subclass the :class:`_expression.Selectable` class are considered to be usable as "selectables" when using SQLAlchemy Core.  The two most common constructs are that of the :class:`_schema.Table` and that of the :class:`_expression.Select` statement.

        SQLAlchemyで使用される用語で、行の集合を表すSQL構文を表します。 :term:`relational algebra` の"リレーション"の概念とほぼ同じです。SQLAlchemyでは、 :class:`_expression.Selectable` クラスをサブクラス化したオブジェクトは、SQLAlchemy Coreを使用するときに"selectables"として使用できると見なされます。最も一般的な2つの構文は、 :class:`_schema.Table` と :class:`_expression.Select` 文の構文です。


    ORM-annotated
    annotations

        .. The phrase "ORM-annotated" refers to an internal aspect of SQLAlchemy, where a Core object such as a :class:`_schema.Column` object can carry along additional runtime information that marks it as belonging to a particular ORM mapping.   The term should not be confused with the common phrase "type annotation", which refers to Python source code "type hints" used for static typing as introduced at :pep:`484`.

        "ORM-annotated"というフレーズは、SQLAlchemyの内部的な側面を指します。ここでは、 :class:`_schema.Column` オブジェクトのようなCoreオブジェクトは、特定のORMマッピングに属することを示す追加の実行時情報を持つことができます。この用語は、 :pep:`484` で紹介された静的型付けに使用されるPythonソースコードの"型ヒント"を指す一般的なフレーズ"型アノテーション"と混同しないでください。

        .. Most of SQLAlchemy's documented code examples are formatted with a small note regarding "Annotated Example" or "Non-annotated Example".  This refers to whether or not the example is :pep:`484` annotated, and is not related to the SQLAlchemy concept of "ORM-annotated".

        SQLAlchemyの文書化されたコード例のほとんどは、"Annotated Example"または"Non-annotated Example"に関する小さな注記でフォーマットされています。これは例が :pep:`484` 注釈付きであるかどうかを示し、"ORM-annotated"というSQLAlchemyの概念とは関係ありません。


        .. When the phrase "ORM-annotated" appears in documentation, it is referring to Core SQL expression objects such as :class:`.Table`, :class:`.Column`, and :class:`.Select` objects, which originate from, or refer to sub-elements that originate from, one or more ORM mappings, and therefore will have ORM-specific interpretations and/or behaviors when passed to ORM methods such as :meth:`_orm.Session.execute`.  For example, when we construct a :class:`.Select` object from an ORM mapping, such as the ``User`` class illustrated in the :ref:`ORM Tutorial <tutorial_declaring_mapped_classes>`::

        ドキュメントに"ORM-annotated"というフレーズがある場合、これは :class:`.Table` 、 :class:`.Column` 、 :class:`.Select` オブジェクトなどのコアSQL式オブジェクトを参照しています。これらのオブジェクトは、1つまたは複数のORMマッピングから生成されるか、またはORMマッピングから生成されるサブ要素を参照します。したがって、 :meth:`_orm.Session.execute` などのORMメソッドに渡されると、ORM固有の解釈や動作が行われます。たとえば、 :ref:`ORM Tutorial<tutorial_declaring_mapped_classes>` に示されている ``User`` クラスのようなORMマッピングから :class:`.Select` オブジェクトを構築する場合::


            >>> stmt = select(User)

        .. The internal state of the above :class:`.Select` refers to the :class:`.Table` to which ``User`` is mapped.   The ``User`` class itself is not immediately referenced.  This is how the :class:`.Select` construct remains compatible with Core-level processes (note that the ``._raw_columns`` member of :class:`.Select` is private and should not be accessed by end-user code)::

        上記の :class:`.Select` の内部状態は、"User"がマップされている :class:`.Table` を参照しています。"User"クラス自体はすぐには参照されません。このようにして、 :class:`.Select` 構文はコアレベルのプロセスと互換性を保っています( :class:`.Select` の ``._raw_columns`` メンバーはprivateであり、エンドユーザコードからはアクセスできないことに注意してください)::

            >>> stmt._raw_columns
            [Table('user_account', MetaData(), Column('id', Integer(), ...)]

        .. However, when our :class:`.Select` is passed along to an ORM :class:`.Session`, the ORM entities that are indirectly associated with the object are used to interpret this :class:`.Select` in an ORM context. The actual "ORM annotations" can be seen in another private variable ``._annotations``::

しかし、 :class:`.Select` がORM :class:`.Session` に渡されると、オブジェクトに間接的に関連付けられたORMエンティティが、この :class:`.Select` をORMコンテキストで解釈するために使用されます。実際の"ORMアノテーション"は、別のプライベート変数 ``._annotations`` で確認することができます。


          >>> stmt._raw_columns[0]._annotations
          immutabledict({
            'entity_namespace': <Mapper at 0x7f4dd8098c10; User>,
            'parententity': <Mapper at 0x7f4dd8098c10; User>,
            'parentmapper': <Mapper at 0x7f4dd8098c10; User>
          })

        .. Therefore we refer to ``stmt`` as an **ORM-annotated select()** object.  It's a :class:`.Select` statement that contains additional information that will cause it to be interpreted in an ORM-specific way when passed to methods like :meth:`_orm.Session.execute`.

        したがって、ここでは ``stmt`` を **ORMアノテーション付きのselect()** オブジェクトと呼びます。これは :class:`.Select` 文で、 :meth:`_orm.Session.execute` のようなメソッドに渡されたときにORM固有の方法で解釈される追加情報を含んでいます。

    plugin
    plugin-enabled
    plugin-specific
        .. "plugin-enabled" or "plugin-specific" generally indicates a function or method in SQLAlchemy Core which will behave differently when used in an ORM context.

        "plugin-enabled"または"plugin-specific"は一般に、SQLAlchemy Coreの関数またはメソッドがORMコンテキストで使用された場合の動作が異なることを示します。


        .. SQLAlchemy allows Core constructs such as :class:`_sql.Select` objects to participate in a "plugin" system, which can inject additional behaviors and features into the object that are not present by default.

        SQLAlchemyでは、 :class:`_sql.Select` オブジェクトのようなCore構成体を"プラグイン"システムに参加させることができ、デフォルトでは存在しない追加の振る舞いや機能をオブジェクトに注入することができます。

        .. Specifically, the primary "plugin" is the "orm" plugin, which is at the base of the system that the SQLAlchemy ORM makes use of Core constructs in order to compose and execute SQL queries that return ORM results.

        具体的には、主要な"プラグイン"は"orm"プラグインであり、SQLAlchemy ORMがORM結果を返すSQLクエリを作成して実行するためにCoreコンストラクトを利用するシステムのベースにあります。

        .. seealso::

            :ref:`migration_20_unify_select`

    crud
    CRUD
        .. An acronym meaning "Create, Update, Delete".  The term in SQL refers to the set of operations that create, modify and delete data from the database, also known as :term:`DML`, and typically refers to the ``INSERT``, ``UPDATE``, and ``DELETE`` statements.

        "Create, Update, Delete"を意味する頭字語。SQLにおけるこの用語は、データベースからデータを作成、変更、削除する操作の集合を指し、 :term:`DML` としても知られています。また、一般的には、 ``INSERT`` 、``UPDATE`` 、 ``DELETE`` 文を指します。

    executemany
        .. This term refers to a part of the :pep:`249` DBAPI specification indicating a single SQL statement that may be invoked against a database connection with multiple parameter sets. The specific method is known as `cursor.executemany() <https://peps.python.org/pep-0249/#executemany>`_, and it has many behavioral differences in comparison to the `cursor.execute() <https://peps.python.org/pep-0249/#execute>`_ method which is used for single-statement invocation. The "executemany" method executes the given SQL statement multiple times, once for each set of parameters passed. The general rationale for using executemany is that of improved performance, wherein the DBAPI may use techniques such as preparing the statement just once beforehand, or otherwise optimizing for invoking the same statement many times.

        この用語は、 :pep:`249` DBAPI仕様の一部で、複数のパラメータセットを持つデータベース接続に対して呼び出すことができる単一のSQL文を示します。この特定のメソッドは `cursor.executemany() <https://peps.python.org/pep-0249/#executemany>`_ として知られており、単一文の呼び出しに使用される `cursor.execute() <https://peps.python.org/pep-0249/#execute>`_ メソッドと比較して、多くの動作上の違いがあります。"executemany"メソッドは、渡されたパラメータセットごとに1回ずつ、指定されたSQL文を複数回実行します。executemanyを使用する一般的な理由は、パフォーマンスを向上させるためです。DBAPIは、事前に1回だけ文を準備したり、同じ文を複数回呼び出すように最適化するなどのテクニックを使用できます。

        .. SQLAlchemy typically makes use of the ``cursor.executemany()`` method automatically when the :meth:`_engine.Connection.execute` method is used where a list of parameter dictionaries were passed; this indicates to SQLAlchemy Core that the SQL statement and processed parameter sets should be passed to ``cursor.executemany()``, where the statement will be invoked by the driver for each parameter dictionary individually.

        パラメータ辞書のリストが渡されたところで :meth:`_engine.Connection.execute` メソッドが使われると、SQLAlchemyは通常自動的に ``cursor.executemany()`` メソッドを利用します。これはSQLAlchemy Coreに対して、SQL文と処理されたパラメータセットを ``cursor.executemany()`` に渡す必要があることを示します。この場合、ドライバはパラメータ辞書ごとに個別にこの文を呼び出します。

        .. A key limitation of the ``cursor.executemany()`` method as used with all known DBAPIs is that the ``cursor`` is not configured to return rows when this method is used.  For **most** backends (a notable exception being the cx_Oracle, / OracleDB DBAPIs), this means that statements like ``INSERT..RETURNING`` typically cannot be used with ``cursor.executemany()`` directly, since DBAPIs typically do not aggregate the single row from each INSERT execution together.

        既知のすべてのDB APIで使用されている ``cursor.executemany()`` メソッドの主な制限は、このメソッドを使用したときに ``cursor`` が行を返すように設定されていないことです。 **ほとんどの** バックエンド(cx_Oracle、/OracleDB DB APIは顕著な例外です)では、これは ``INSERT.RETURNING`` のような文は通常 ``cursor.executemany()`` と直接使用できないことを意味します。なぜなら、DB APIは通常、各INSERT実行から単一の行を集約しないからです。

        .. To overcome this limitation, SQLAlchemy as of the 2.0 series implements an alternative form of "executemany" which is known as :ref:`engine_insertmanyvalues`. This feature makes use of ``cursor.execute()`` to invoke an INSERT statement that will proceed with multiple parameter sets in one round trip, thus producing the same effect as using ``cursor.executemany()`` while still supporting RETURNING.

        この制限を克服するために、2.0シリーズのSQLAlchemyは :ref:`engine_insertmanyvalues` として知られる別の形式の"executemany"を実装しています。この機能は、 ``cursor.execute()`` を使用して、1回のラウンドトリップで複数のパラメータセットを処理するINSERT文を呼び出します。したがって、RETURNINGをサポートしながら、 ``cursor.executemany()`` を使用した場合と同じ効果が得られます。


        .. seealso::

            .. :ref:`tutorial_multiple_parameters` - tutorial introduction to "executemany"

            :ref:`tutorial_multiple_parameters` - "executemany"のチュートリアル入門

            .. :ref:`engine_insertmanyvalues` - SQLAlchemy feature which allows RETURNING to be used with "executemany"

            :ref:`engine_insertmanyvalues` - RETURNINGを"executemany"で使用できるようにするSQLAlchemyの機能


    marshalling
    data marshalling
        ..  The process of transforming the memory representation of an object to a data format suitable for storage or transmission to another part of a system, when data must be moved between different parts of a computer program or from one program to another. In terms of SQLAlchemy, we often need to "marshal" data into a format appropriate for passing into the relational database.

        コンピュータプログラムの異なる部分間で、またはあるプログラムから別のプログラムにデータを移動する必要がある場合に、オブジェクトのメモリ表現を、システムの別の部分への格納または転送に適したデータ形式に変換するプロセス。SQLAlchemyに関しては、リレーショナル・データベースに渡すのに適した形式にデータを「マーシャリング」する必要があります。

         .. seealso::

            `Marshalling (via Wikipedia) <https://en.wikipedia.org/wiki/Marshalling_(computer_science)>`_

            .. :ref:`types_typedecorator` - SQLAlchemy's :class:`.TypeDecorator` is commonly used for data marshalling as data is sent into the database for INSERT and UPDATE statements, and "unmarshalling" data as it is retrieved using SELECT statements.

            :ref:`types_TypeDecorator` - SQLAlchemyの :class:`.TypeDecorator` は、データがINSERT文とUPDATE文のためにデータベースに送られるときのデータのマーシャリングと、SELECT文を使って取得されるときのデータの"アンマーシャリング"によく使われます。

    descriptor
    descriptors

        .. In Python, a descriptor is an object attribute with “binding behavior”, one whose attribute access has been overridden by methods in the `descriptor protocol <https://docs.python.org/howto/descriptor.html>`_.  Those methods are ``__get__()``, ``__set__()``, and ``__delete__()``.  If any of those methods are defined for an object, it is said to be a descriptor.

        Pythonでは、記述子は「バインド動作」を持つオブジェクト属性であり、その属性アクセスは `descriptor protocol <https://docs.python.org/howto/descriptor.html>`_.  のメソッドによってオーバーライドされています。これらのメソッドは、 ``__get__()`` 、``__set__()`` 、および ``__delete__()`` です。これらのメソッドのいずれかがオブジェクトに対して定義されている場合、それは記述子であると言われます。

        .. In SQLAlchemy, descriptors are used heavily in order to provide attribute behavior on mapped classes. When a class is mapped as such::

        SQLAlchemyでは、記述子は、マップされたクラスに対して属性の動作を提供するために頻繁に使用されます。クラスが次のようにマップされる場合::


            class MyClass(Base):
                __tablename__ = "foo"

                id = Column(Integer, primary_key=True)
                data = Column(String)

        .. The ``MyClass`` class will be :term:`mapped` when its definition is complete, at which point the ``id`` and ``data`` attributes, starting out as :class:`_schema.Column` objects, will be replaced by the :term:`instrumentation` system with instances of :class:`.InstrumentedAttribute`, which are descriptors that provide the above mentioned ``__get__()``, ``__set__()`` and ``__delete__()`` methods.   The :class:`.InstrumentedAttribute` will generate a SQL expression when used at the class level:

        定義が完了すると、 ``MyClass`` クラスは :term:`mapped` になります。その時点で、 :class:`_schema.Column` オブジェクトから始まる ``id`` 属性と ``data`` 属性は、 :class:`.InstrumentedAttribute` のインスタンスを持つ :term:`instrumentation` システムに置き換えられます。これは、前述の ``__get__()`` 、 ``__set__()`` 、 ``__delete__()`` メソッドを提供する記述子です。 :class:`.InstrumentedAttribute` をクラスレベルで使用すると、SQL式が生成されます。


        .. sourcecode:: pycon+sql

            >>> print(MyClass.data == 5)
            {printsql}data = :data_1

        and at the instance level, keeps track of changes to values, and also :term:`lazy loads` unloaded attributes from the database::

            >>> m1 = MyClass()
            >>> m1.id = 5
            >>> m1.data = "some data"

            >>> from sqlalchemy import inspect
            >>> inspect(m1).attrs.data.history.added
            "some data"

    DDL
        An acronym for **Data Definition Language**.  DDL is the subset of SQL that relational databases use to configure tables, constraints, and other permanent objects within a database schema. SQLAlchemy provides a rich API for constructing and emitting DDL expressions.

        .. seealso::

            :ref:`metadata_toplevel`

            `DDL (via Wikipedia) <https://en.wikipedia.org/wiki/Data_definition_language>`_

            :term:`DML`

            :term:`DQL`

    DML
       An acronym for **Data Manipulation Language**.  DML is the subset of SQL that relational databases use to *modify* the data in tables. DML typically refers to the three widely familiar statements of INSERT, UPDATE and  DELETE, otherwise known as :term:`CRUD` (acronym for "Create, Read, Update, Delete").

        .. seealso::

            `DML (via Wikipedia) <https://en.wikipedia.org/wiki/Data_manipulation_language>`_

            :term:`DDL`

            :term:`DQL`

    DQL
        An acronym for **Data Query Language**. DQL is the subset of SQL that relational databases use to *read* the data in tables.  DQL almost exclusively refers to the SQL SELECT construct as the top level SQL statement in use.

        .. seealso::

            `DQL (via Wikipedia) <https://en.wikipedia.org/wiki/Data_query_language>`_

            :term:`DML`

            :term:`DDL`

    metadata
    database metadata
    table metadata
        The term "metadata" generally refers to "data that describes data"; data that itself represents the format and/or structure of some other kind of data.  In SQLAlchemy, the term "metadata" typically refers  to the :class:`_schema.MetaData` construct, which is a collection of information about the tables, columns, constraints, and other :term:`DDL` objects that may exist in a particular database.

        .. seealso::

            `Metadata Mapping (via Martin Fowler) <https://www.martinfowler.com/eaaCatalog/metadataMapping.html>`_

            :ref:`tutorial_working_with_metadata`  - in the :ref:`unified_tutorial`

    version id column
        In SQLAlchemy, this refers to the use of a particular table column that tracks the "version" of a particular row, as the row changes values.   While there are different kinds of relational patterns that make use of a "version id column" in different ways, SQLAlchemy's ORM includes a particular feature that allows for such a column to be configured as a means of testing for stale data when a row is being UPDATEd with new information. If the last known "version" of this column does not match that of the row when we try to put new data into the row, we know that we are acting on stale information.

        There are also other ways of storing "versioned" rows in a database, often referred to as "temporal" data.  In addition to SQLAlchemy's versioning feature, a few more examples are also present in the documentation, see the links below.

        .. seealso::

            :ref:`mapper_version_counter` - SQLAlchemy's built-in version id feature.

            :ref:`examples_versioning` - other examples of mappings that version rows
            temporally.

    registry
        An object, typically globally accessible, that contains long-lived information about some program state that is generally useful to many parts of a program.

        .. seealso::

            `Registry (via Martin Fowler) <https://martinfowler.com/eaaCatalog/registry.html>`_

    cascade
        A term used in SQLAlchemy to describe how an ORM persistence action that takes place on a particular object would extend into other objects which are directly associated with that object. In SQLAlchemy, these object associations are configured using the :func:`_orm.relationship` construct. :func:`_orm.relationship` contains a parameter called :paramref:`_orm.relationship.cascade` which provides options on how certain persistence operations may cascade.

        The term "cascades" as well as the general architecture of this system in SQLAlchemy was borrowed, for better or worse, from the Hibernate ORM.

        .. seealso::

            :ref:`unitofwork_cascades`

    dialect
        In SQLAlchemy, the "dialect" is a Python object that represents information and methods that allow database operations to proceed on a particular kind of database backend and a particular kind of Python driver (or :term:`DBAPI`) for that database. SQLAlchemy dialects are subclasses of the :class:`.Dialect` class.

        .. seealso::

            :ref:`engines_toplevel`

    discriminator
        A result-set column which is used during :term:`polymorphic` loading to determine what kind of mapped class should be applied to a particular incoming result row.

        .. seealso::

            :ref:`inheritance_toplevel`

    instrumentation
    instrumented
    instrumenting
        Instrumentation refers to the process of augmenting the functionality and attribute set of a particular class. Ideally, the behavior of the class should remain close to a regular class, except that additional behaviors and features are made available. The SQLAlchemy :term:`mapping` process, among other things, adds database-enabled :term:`descriptors` to a mapped class each of which represents a particular database column or relationship to a related class.

    identity key
        A key associated with ORM-mapped objects that identifies their primary key identity within the database, as well as their unique identity within a :class:`_orm.Session` :term:`identity map`.

        In SQLAlchemy, you can view the identity key for an ORM object using the :func:`_sa.inspect` API to return the :class:`_orm.InstanceState` tracking object, then looking at the :attr:`_orm.InstanceState.key` attribute::

            >>> from sqlalchemy import inspect
            >>> inspect(some_object).key
            (<class '__main__.MyTable'>, (1,), None)

        .. seealso::

           :term:`identity map`

    identity map
        A mapping between Python objects and their database identities. The identity map is a collection that's associated with an ORM :term:`Session` object, and maintains a single instance of every database object keyed to its identity. The advantage to this pattern is that all operations which occur for a particular database identity are transparently coordinated onto a single object instance.  When using an identity map in conjunction with an :term:`isolated` transaction, having a reference to an object that's known to have a particular primary key can be considered from a practical standpoint to be a proxy to the actual database row.

        .. seealso::

            `Identity Map (via Martin Fowler) <https://martinfowler.com/eaaCatalog/identityMap.html>`_

            :ref:`session_get` - how to look up an object in the identity map by primary key

    lazy initialization
        A tactic of delaying some initialization action, such as creating objects, populating data, or establishing connectivity to other services, until those resources are required.

        .. seealso::

            `Lazy initialization (via Wikipedia) <https://en.wikipedia.org/wiki/Lazy_initialization>`_

    lazy load
    lazy loads
    lazy loaded
    lazy loading
        In object relational mapping, a "lazy load" refers to an attribute that does not contain its database-side value for some period of time, typically when the object is first loaded. Instead, the attribute receives a *memoization* that causes it to go out to the database and load its data when it's first used. Using this pattern, the complexity and time spent within object fetches can sometimes be reduced, in that attributes for related tables don't need to be addressed immediately.

        Lazy loading is the opposite of :term:`eager loading`.

        Within SQLAlchemy, lazy loading is a key feature of the ORM, and applies to attributes which are :term:`mapped` on a user-defined class. When attributes that refer to database columns or related objects are accessed, for which no loaded value is present, the ORM makes use of the :class:`_orm.Session` for which the current object is associated with in the :term:`persistent` state, and emits a SELECT statement on the current transaction, starting a new transaction if one was not in progress. If the object is in the :term:`detached` state and not associated with any :class:`_orm.Session`, this is considered to be an error state and an :ref:`informative exception <error_bhk3>` is raised.

        .. seealso::

            `Lazy Load (via Martin Fowler) <https://martinfowler.com/eaaCatalog/lazyLoad.html>`_

            :term:`N plus one problem`

            :ref:`loading_columns` - includes information on lazy loading of ORM mapped columns

            :doc:`orm/queryguide/relationships` - includes information on lazy loading of ORM related objects

            :ref:`asyncio_orm_avoid_lazyloads` - tips on avoiding lazy loading when using the :ref:`asyncio_toplevel` extension

    eager load
    eager loads
    eager loaded
    eager loading
    eagerly load
        In object relational mapping, an "eager load" refers to an attribute that is populated with its database-side value at the same time as when the object itself is loaded from the database. In SQLAlchemy, the term "eager loading" usually refers to related collections and instances of objects that are linked between mappings using the :func:`_orm.relationship` construct, but can also refer to additional column attributes being loaded, often from other tables related to a particular table being queried, such as when using :ref:`inheritance <inheritance_toplevel>` mappings.

        Eager loading is the opposite of :term:`lazy loading`.

        .. seealso::

            :doc:`orm/queryguide/relationships`


    mapping
    mapped
    mapped class
    ORM mapped class
        We say a class is "mapped" when it has been associated with an instance of the :class:`_orm.Mapper` class. This process associates the class with a database table or other :term:`selectable` construct, so that instances of it can be persisted and loaded using a :class:`.Session`.

        .. seealso::

            :ref:`orm_mapping_classes_toplevel`

    N plus one problem
    N plus one
        The N plus one problem is a common side effect of the :term:`lazy load` pattern, whereby an application wishes to iterate through a related attribute or collection on each member of a result set of objects, where that attribute or collection is set to be loaded via the lazy load pattern. The net result is that a SELECT statement is emitted to load the initial result set of parent objects; then, as the application iterates through each member, an additional SELECT statement is emitted for each member in order to load the related attribute or collection for that member. The end result is that for a result set of N parent objects, there will be N + 1 SELECT statements emitted.

        The N plus one problem is alleviated using :term:`eager loading`.

        .. seealso::

            :ref:`tutorial_orm_loader_strategies`

            :doc:`orm/queryguide/relationships`

    polymorphic
    polymorphically
        Refers to a function that handles several types at once. In SQLAlchemy, the term is usually applied to the concept of an ORM mapped class whereby a query operation will return different subclasses based on information in the result set, typically by checking the value of a particular column in the result known as the :term:`discriminator`.

        Polymorphic loading in SQLAlchemy implies that a one or a combination of three different schemes are used to map a hierarchy of classes; "joined", "single", and "concrete". The section :ref:`inheritance_toplevel` describes inheritance mapping fully.

    method chaining
    generative
        "Method chaining", referred to within SQLAlchemy documentation as "generative", is an object-oriented technique whereby the state of an object is constructed by calling methods on the object. The object features any number of methods, each of which return a new object (or in some cases the same object) with additional state added to the object.

        The two SQLAlchemy objects that make the most use of method chaining are the :class:`_expression.Select` object and the :class:`.orm.query.Query` object.  For example, a :class:`_expression.Select` object can be assigned two expressions to its WHERE clause as well as an ORDER BY clause by calling upon the :meth:`_expression.Select.where` and :meth:`_expression.Select.order_by` methods::

            stmt = (
                select(user.c.name)
                .where(user.c.id > 5)
                .where(user.c.name.like("e%"))
                .order_by(user.c.name)
            )

        Each method call above returns a copy of the original
        :class:`_expression.Select` object with additional qualifiers
        added.

    release
    releases
    released
        In the context of SQLAlchemy, the term "released" refers to the process of ending the usage of a particular database connection.  SQLAlchemy features the usage of connection pools, which allows configurability as to the lifespan of database connections. When using a pooled connection, the process of "closing" it, i.e. invoking a statement like ``connection.close()``, may have the effect of the connection being returned to an existing pool, or it may have the effect of actually shutting down the underlying TCP/IP connection referred to by that connection - which one takes place depends on configuration as well as the current state of the pool. So we used the term *released* instead, to mean "do whatever it is you do with connections when we're done using them".

        The term will sometimes be used in the phrase, "release transactional resources", to indicate more explicitly that what we are actually "releasing" is any transactional state which as accumulated upon the connection. In most situations, the process of selecting from tables, emitting updates, etc. acquires :term:`isolated` state upon that connection as well as potential row or table locks. This state is all local to a particular transaction on the connection, and is released when we emit a rollback. An important feature of the connection pool is that when we return a connection to the pool, the ``connection.rollback()`` method of the DBAPI is called as well, so that as the connection is set up to be used again, it's in a "clean" state with no references held to the previous series of operations.

        .. seealso::

            :ref:`pooling_toplevel`

    DBAPI
    pep-249
        DBAPI is shorthand for the phrase "Python Database API Specification".  This is a widely used specification within Python to define common usage patterns for all database connection packages. The DBAPI is a "low level" API which is typically the lowest level system used in a Python application to talk to a database.  SQLAlchemy's :term:`dialect` system is constructed around the operation of the DBAPI, providing individual dialect classes which service a specific DBAPI on top of a specific database engine; for example, the :func:`_sa.create_engine` URL ``postgresql+psycopg2://@localhost/test`` refers to the :mod:`psycopg2 <.postgresql.psycopg2>` DBAPI/dialect combination, whereas the URL ``mysql+mysqldb://@localhost/test`` refers to the :mod:`MySQL for Python <.mysql.mysqldb>` DBAPI/dialect combination.

        .. seealso::

            `PEP 249 - Python Database API Specification v2.0 <https://www.python.org/dev/peps/pep-0249/>`_

    domain model

        A domain model in problem solving and software engineering is a conceptual model of all the topics related to a specific problem. It describes the various entities, their attributes, roles, and relationships, plus the constraints that govern the problem domain.

        (via Wikipedia)

        .. seealso::

            `Domain Model (via Wikipedia) <https://en.wikipedia.org/wiki/Domain_model>`_

    unit of work
        A software architecture where a persistence system such as an object relational mapper maintains a list of changes made to a series of objects, and periodically flushes all those pending changes out to the database.

        SQLAlchemy's :class:`_orm.Session` implements the unit of work pattern, where objects that are added to the :class:`_orm.Session` using methods like :meth:`_orm.Session.add` will then participate in unit-of-work style persistence.

        For a walk-through of what unit of work persistence looks like in SQLAlchemy, start with the section :ref:`tutorial_orm_data_manipulation` in the :ref:`unified_tutorial`.  Then for more detail, see :ref:`session_basics` in the general reference documentation.

        .. seealso::

            `Unit of Work (via Martin Fowler) <https://martinfowler.com/eaaCatalog/unitOfWork.html>`_

            :ref:`tutorial_orm_data_manipulation`

            :ref:`session_basics`

    flush
    flushing
    flushed

        This refers to the actual process used by the :term:`unit of work` to emit changes to a database. In SQLAlchemy this process occurs via the :class:`_orm.Session` object and is usually automatic, but can also be controlled manually.

        .. seealso::

            :ref:`session_flushing`

    expire
    expired
    expires
    expiring
    Expiring
        In the SQLAlchemy ORM, refers to when the data in a :term:`persistent` or sometimes :term:`detached` object is erased, such that when the object's attributes are next accessed, a :term:`lazy load` SQL query will be emitted in order to refresh the data for this object as stored in the current ongoing transaction.

        .. seealso::

            :ref:`session_expire`

    Session
        The container or scope for ORM database operations. Sessions load instances from the database, track changes to mapped instances and persist changes in a single unit of work when flushed.

        .. seealso::

            :doc:`orm/session`

    columns clause
        The portion of the ``SELECT`` statement which enumerates the SQL expressions to be returned in the result set. The expressions follow the ``SELECT`` keyword directly and are a comma-separated list of individual expressions.

        E.g.:

        .. sourcecode:: sql

            SELECT user_account.name, user_account.email
            FROM user_account WHERE user_account.name = 'fred'

        Above, the list of columns ``user_acount.name``, ``user_account.email`` is the columns clause of the ``SELECT``.

    WHERE clause
        The portion of the ``SELECT`` statement which indicates criteria by which rows should be filtered. It is a single SQL expression which follows the keyword ``WHERE``.

        .. sourcecode:: sql

            SELECT user_account.name, user_account.email
            FROM user_account
            WHERE user_account.name = 'fred' AND user_account.status = 'E'

        Above, the phrase ``WHERE user_account.name = 'fred' AND user_account.status = 'E'`` comprises the WHERE clause of the ``SELECT``.

    FROM clause
        The portion of the ``SELECT`` statement which indicates the initial source of rows.

        A simple ``SELECT`` will feature one or more table names in its FROM clause. Multiple sources are separated by a comma:

        .. sourcecode:: sql

            SELECT user.name, address.email_address
            FROM user, address
            WHERE user.id=address.user_id

        The FROM clause is also where explicit joins are specified. We can rewrite the above ``SELECT`` using a single ``FROM`` element which consists of a ``JOIN`` of the two tables:

        .. sourcecode:: sql

            SELECT user.name, address.email_address
            FROM user JOIN address ON user.id=address.user_id


    subquery
    scalar subquery
        Refers to a ``SELECT`` statement that is embedded within an enclosing ``SELECT``.

        A subquery comes in two general flavors, one known as a "scalar select" which specifically must return exactly one row and one column, and the other form which acts as a "derived table" and serves as a source of rows for the FROM clause of another select. A scalar select is eligible to be placed in the :term:`WHERE clause`, :term:`columns clause`, ORDER BY clause or HAVING clause of the enclosing select, whereas the derived table form is eligible to be placed in the FROM clause of the enclosing ``SELECT``.

        Examples:

        1. a scalar subquery placed in the :term:`columns clause` of an enclosing ``SELECT``. The subquery in this example is a :term:`correlated subquery` because part of the rows which it selects from are given via the enclosing statement.

           .. sourcecode:: sql

            SELECT id, (SELECT name FROM address WHERE address.user_id=user.id)
            FROM user

        2. a scalar subquery placed in the :term:`WHERE clause` of an enclosing ``SELECT``. This subquery in this example is not correlated as it selects a fixed result.

           .. sourcecode:: sql

            SELECT id, name FROM user
            WHERE status=(SELECT status_id FROM status_code WHERE code='C')

        3. a derived table subquery placed in the :term:`FROM clause` of an enclosing ``SELECT``.  Such a subquery is almost always given an alias name.

           .. sourcecode:: sql

            SELECT user.id, user.name, ad_subq.email_address
            FROM
                user JOIN
                (select user_id, email_address FROM address WHERE address_type='Q') AS ad_subq
                ON user.id = ad_subq.user_id

    correlates
    correlated subquery
    correlated subqueries
        A :term:`subquery` is correlated if it depends on data in the enclosing ``SELECT``.

        Below, a subquery selects the aggregate value ``MIN(a.id)`` from the ``email_address`` table, such that it will be invoked for each value of ``user_account.id``, correlating the value of this column against the ``email_address.user_account_id`` column:

        .. sourcecode:: sql

            SELECT user_account.name, email_address.email
             FROM user_account
             JOIN email_address ON user_account.id=email_address.user_account_id
             WHERE email_address.id = (
                SELECT MIN(a.id) FROM email_address AS a
                WHERE a.user_account_id=user_account.id
             )

        The above subquery refers to the ``user_account`` table, which is not itself in the ``FROM`` clause of this nested query.  Instead, the ``user_account`` table is received from the enclosing query, where each row selected from ``user_account`` results in a distinct execution of the subquery.

        A correlated subquery is in most cases present in the :term:`WHERE clause` or :term:`columns clause` of the immediately enclosing ``SELECT`` statement, as well as in the ORDER BY or HAVING clause.

        In less common cases, a correlated subquery may be present in the :term:`FROM clause` of an enclosing ``SELECT``; in these cases the correlation is typically due to the enclosing ``SELECT`` itself being enclosed in the WHERE, ORDER BY, columns or HAVING clause of another ``SELECT``, such as:

        .. sourcecode:: sql

            SELECT parent.id FROM parent
            WHERE EXISTS (
                SELECT * FROM (
                    SELECT child.id AS id, child.parent_id AS parent_id, child.pos AS pos
                    FROM child
                    WHERE child.parent_id = parent.id ORDER BY child.pos
                LIMIT 3)
            WHERE id = 7)

        Correlation from one ``SELECT`` directly to one which encloses the correlated query via its ``FROM`` clause is not possible, because the correlation can only proceed once the original source rows from the enclosing statement's FROM clause are available.


    ACID
    ACID model
        An acronym for "Atomicity, Consistency, Isolation, Durability"; a set of properties that guarantee that database transactions are processed reliably.  (via Wikipedia)

        .. seealso::

            :term:`atomicity`

            :term:`consistency`

            :term:`isolation`

            :term:`durability`

            `ACID Model (via Wikipedia) <https://en.wikipedia.org/wiki/ACID_Model>`_

    atomicity
        Atomicity is one of the components of the :term:`ACID` model, and requires that each transaction is "all or nothing": if one part of the transaction fails, the entire transaction fails, and the database state is left unchanged. An atomic system must guarantee atomicity in each and every situation, including power failures, errors, and crashes.  (via Wikipedia)

        .. seealso::

            :term:`ACID`

            `Atomicity (via Wikipedia) <https://en.wikipedia.org/wiki/Atomicity_(database_systems)>`_

    consistency
        Consistency is one of the components of the :term:`ACID` model, and ensures that any transaction will bring the database from one valid state to another. Any data written to the database must be valid according to all defined rules, including but not limited to :term:`constraints`, cascades, triggers, and any combination thereof.  (via Wikipedia)

        .. seealso::

            :term:`ACID`

            `Consistency (via Wikipedia) <https://en.wikipedia.org/wiki/Consistency_(database_systems)>`_

    isolation
    isolated
    isolation level
        The isolation property of the :term:`ACID` model ensures that the concurrent execution of transactions results in a system state that would be obtained if transactions were executed serially, i.e. one after the other. Each transaction must execute in total isolation i.e. if T1 and T2 execute concurrently then each should remain independent of the other.  (via Wikipedia)

        .. seealso::

            :term:`ACID`

            `Isolation (via Wikipedia) <https://en.wikipedia.org/wiki/Isolation_(database_systems)>`_

            :term:`read uncommitted`

            :term:`read committed`

            :term:`repeatable read`

            :term:`serializable`

    repeatable read
        One of the four database :term:`isolation` levels, repeatable read features all of the isolation of :term:`read committed`, and additionally features that any particular row that is read within a transaction is guaranteed from that point to not have any subsequent external changes in value (i.e. from other concurrent UPDATE statements) for the duration of that transaction.

    read committed
        One of the four database :term:`isolation` levels, read committed features that the transaction will not be exposed to any data from other concurrent transactions that has not been committed yet, preventing so-called "dirty reads".  However, under read committed there can be non-repeatable reads, meaning data in a row may change when read a second time if another transaction has committed changes.

    read uncommitted
        One of the four database :term:`isolation` levels, read uncommitted features that changes made to database data within a transaction will not become permanent until the transaction is committed. However, within read uncommitted, it may be possible for data that is not committed in other transactions to be viewable within the scope of another transaction; these are known as "dirty reads".

    serializable
        One of the four database :term:`isolation` levels, serializable features all of the isolation of :term:`repeatable read`, and additionally within a lock-based approach guarantees that so-called "phantom reads" cannot occur; this means that rows which are INSERTed or DELETEd within the scope of other transactions will not be detectable within this transaction.  A row that is read within this transaction is guaranteed to continue existing, and a row that does not exist is guaranteed that it cannot appear of inserted from another transaction.

        Serializable isolation typically relies upon locking of rows or ranges of rows in order to achieve this effect and can increase the chance of deadlocks and degrade performance. There are also non-lock based schemes however these necessarily rely upon rejecting transactions if write collisions are detected.


    durability
        Durability is a property of the :term:`ACID` model which means that once a transaction has been committed, it will remain so, even in the event of power loss, crashes, or errors. In a relational database, for instance, once a group of SQL statements execute, the results need to be stored permanently (even if the database crashes immediately thereafter).  (via Wikipedia)

        .. seealso::

            :term:`ACID`

            `Durability (via Wikipedia) <https://en.wikipedia.org/wiki/Durability_(database_systems)>`_

    RETURNING
        This is a non-SQL standard clause provided in various forms by certain backends, which provides the service of returning a result set upon execution of an INSERT, UPDATE or DELETE statement. Any set of columns from the matched rows can be returned, as though they were produced from a SELECT statement.

        The RETURNING clause provides both a dramatic performance boost to common update/select scenarios, including retrieval of inline- or default- generated primary key values and defaults at the moment they were created, as well as a way to get at server-generated default values in an atomic way.

        An example of RETURNING, idiomatic to PostgreSQL, looks like:

        .. sourcecode:: sql

            INSERT INTO user_account (name) VALUES ('new name') RETURNING id, timestamp

        Above, the INSERT statement will provide upon execution a result set which includes the values of the columns ``user_account.id`` and ``user_account.timestamp``, which above should have been generated as default values as they are not included otherwise (but note any series of columns or SQL expressions can be placed into RETURNING, not just default-value columns).

        The backends that currently support RETURNING or a similar construct are PostgreSQL, SQL Server, Oracle, and Firebird.  The PostgreSQL and Firebird implementations are generally full featured, whereas the implementations of SQL Server and Oracle have caveats. On SQL Server, the clause is known as "OUTPUT INSERTED" for INSERT and UPDATE statements and "OUTPUT DELETED" for DELETE statements; the key caveat is that triggers are not supported in conjunction with this keyword.  On Oracle, it is known as "RETURNING...INTO", and requires that the value be placed into an OUT parameter, meaning not only is the syntax awkward, but it can also only be used for one row at a time.

        SQLAlchemy's :meth:`.UpdateBase.returning` system provides a layer of abstraction on top of the RETURNING systems of these backends to provide a consistent interface for returning columns.  The ORM also includes many optimizations that make use of RETURNING when available.

    one to many
        A style of :func:`~sqlalchemy.orm.relationship` which links the primary key of the parent mapper's table to the foreign key of a related table.   Each unique parent object can then refer to zero or more unique related objects.

        The related objects in turn will have an implicit or explicit :term:`many to one` relationship to their parent object.

        An example one to many schema (which, note, is identical to the :term:`many to one` schema):

        .. sourcecode:: sql

            CREATE TABLE department (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30),
                dep_id INTEGER REFERENCES department(id)
            )

        The relationship from ``department`` to ``employee`` is one to many, since many employee records can be associated with a single department. A SQLAlchemy mapping might look like::

            class Department(Base):
                __tablename__ = "department"
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                employees = relationship("Employee")


            class Employee(Base):
                __tablename__ = "employee"
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                dep_id = Column(Integer, ForeignKey("department.id"))

        .. seealso::

            :term:`relationship`

            :term:`many to one`

            :term:`backref`

    many to one
        A style of :func:`~sqlalchemy.orm.relationship` which links a foreign key in the parent mapper's table to the primary key of a related table. Each parent object can then refer to exactly zero or one related object.

        The related objects in turn will have an implicit or explicit :term:`one to many` relationship to any number of parent objects that refer to them.

        An example many to one schema (which, note, is identical to the :term:`one to many` schema):

        .. sourcecode:: sql

            CREATE TABLE department (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30),
                dep_id INTEGER REFERENCES department(id)
            )


        The relationship from ``employee`` to ``department`` is many to one, since many employee records can be associated with a single department. A SQLAlchemy mapping might look like::

            class Department(Base):
                __tablename__ = "department"
                id = Column(Integer, primary_key=True)
                name = Column(String(30))


            class Employee(Base):
                __tablename__ = "employee"
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                dep_id = Column(Integer, ForeignKey("department.id"))
                department = relationship("Department")

        .. seealso::

            :term:`relationship`

            :term:`one to many`

            :term:`backref`

    backref
    bidirectional relationship
        An extension to the :term:`relationship` system whereby two distinct :func:`~sqlalchemy.orm.relationship` objects can be mutually associated with each other, such that they coordinate in memory as changes occur to either side. The most common way these two relationships are constructed is by using the :func:`~sqlalchemy.orm.relationship` function explicitly for one side and specifying the ``backref`` keyword to it so that the other :func:`~sqlalchemy.orm.relationship` is created automatically.  We can illustrate this against the example we've used in :term:`one to many` as follows::

            class Department(Base):
                __tablename__ = "department"
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                employees = relationship("Employee", backref="department")


            class Employee(Base):
                __tablename__ = "employee"
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                dep_id = Column(Integer, ForeignKey("department.id"))

        A backref can be applied to any relationship, including one to many,
        many to one, and :term:`many to many`.

        .. seealso::

            :term:`relationship`

            :term:`one to many`

            :term:`many to one`

            :term:`many to many`

    many to many
        A style of :func:`sqlalchemy.orm.relationship` which links two tables together via an intermediary table in the middle. Using this configuration, any number of rows on the left side may refer to any number of rows on the right, and vice versa.

        A schema where employees can be associated with projects:

        .. sourcecode:: sql

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE project (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee_project (
                employee_id INTEGER PRIMARY KEY,
                project_id INTEGER PRIMARY KEY,
                FOREIGN KEY employee_id REFERENCES employee(id),
                FOREIGN KEY project_id REFERENCES project(id)
            )

        Above, the ``employee_project`` table is the many-to-many table, which naturally forms a composite primary key consisting of the primary key from each related table.

        In SQLAlchemy, the :func:`sqlalchemy.orm.relationship` function can represent this style of relationship in a mostly transparent fashion, where the many-to-many table is specified using plain table metadata::

            class Employee(Base):
                __tablename__ = "employee"

                id = Column(Integer, primary_key=True)
                name = Column(String(30))

                projects = relationship(
                    "Project",
                    secondary=Table(
                        "employee_project",
                        Base.metadata,
                        Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
                        Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
                    ),
                    backref="employees",
                )


            class Project(Base):
                __tablename__ = "project"

                id = Column(Integer, primary_key=True)
                name = Column(String(30))

        Above, the ``Employee.projects`` and back-referencing ``Project.employees`` collections are defined::

            proj = Project(name="Client A")

            emp1 = Employee(name="emp1")
            emp2 = Employee(name="emp2")

            proj.employees.extend([emp1, emp2])

        .. seealso::

            :term:`association relationship`

            :term:`relationship`

            :term:`one to many`

            :term:`many to one`

    relationship
    relationships
        A connecting unit between two mapped classes, corresponding to some relationship between the two tables in the database.

        The relationship is defined using the SQLAlchemy function :func:`~sqlalchemy.orm.relationship`. Once created, SQLAlchemy inspects the arguments and underlying mappings involved in order to classify the relationship as one of three types: :term:`one to many`, :term:`many to one`, or :term:`many to many`.  With this classification, the relationship construct handles the task of persisting the appropriate linkages in the database in response to in-memory object associations, as well as the job of loading object references and collections into memory based on the current linkages in the database.

        .. seealso::

            :ref:`relationship_config_toplevel`

    cursor
        A control structure that enables traversal over the records in a database. In the Python DBAPI, the cursor object is in fact the starting point for statement execution as well as the interface used for fetching results.

        .. seealso::

            `Cursor Objects (in pep-249) <https://www.python.org/dev/peps/pep-0249/#cursor-objects>`_

            `Cursor (via Wikipedia) <https://en.wikipedia.org/wiki/Cursor_(databases)>`_


    association relationship
        A two-tiered :term:`relationship` which links two tables together using an association table in the middle. The association relationship differs from a :term:`many to many` relationship in that the many-to-many table is mapped by a full class, rather than invisibly handled by the :func:`sqlalchemy.orm.relationship` construct as in the case with many-to-many, so that additional attributes are explicitly available.

        For example, if we wanted to associate employees with projects, also storing the specific role for that employee with the project, the relational schema might look like:

        .. sourcecode:: sql

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE project (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee_project (
                employee_id INTEGER PRIMARY KEY,
                project_id INTEGER PRIMARY KEY,
                role_name VARCHAR(30),
                FOREIGN KEY employee_id REFERENCES employee(id),
                FOREIGN KEY project_id REFERENCES project(id)
            )

        A SQLAlchemy declarative mapping for the above might look like::

            class Employee(Base):
                __tablename__ = "employee"

                id = Column(Integer, primary_key=True)
                name = Column(String(30))


            class Project(Base):
                __tablename__ = "project"

                id = Column(Integer, primary_key=True)
                name = Column(String(30))


            class EmployeeProject(Base):
                __tablename__ = "employee_project"

                employee_id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
                project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
                role_name = Column(String(30))

                project = relationship("Project", backref="project_employees")
                employee = relationship("Employee", backref="employee_projects")

        Employees can be added to a project given a role name::

            proj = Project(name="Client A")

            emp1 = Employee(name="emp1")
            emp2 = Employee(name="emp2")

            proj.project_employees.extend(
                [
                    EmployeeProject(employee=emp1, role_name="tech lead"),
                    EmployeeProject(employee=emp2, role_name="account executive"),
                ]
            )

        .. seealso::

            :term:`many to many`

    constraint
    constraints
    constrained
        Rules established within a relational database that ensure the validity and consistency of data. Common forms of constraint include :term:`primary key constraint`, :term:`foreign key constraint`, and :term:`check constraint`.

    candidate key

        A :term:`relational algebra` term referring to an attribute or set of attributes that form a uniquely identifying key for a row.  A row may have more than one candidate key, each of which is suitable for use as the primary key of that row.  The primary key of a table is always a candidate key.

        .. seealso::

            :term:`primary key`

            `Candidate key (via Wikipedia) <https://en.wikipedia.org/wiki/Candidate_key>`_

            https://www.databasestar.com/database-keys/

    primary key
    primary key constraint

        A :term:`constraint` that uniquely defines the characteristics of each row in a table. The primary key has to consist of characteristics that cannot be duplicated by any other row. The primary key may consist of a single attribute or multiple attributes in combination.  (via Wikipedia)

        The primary key of a table is typically, though not always,
        defined within the ``CREATE TABLE`` :term:`DDL`:

        .. sourcecode:: sql

            CREATE TABLE employee (
                 emp_id INTEGER,
                 emp_name VARCHAR(30),
                 dep_id INTEGER,
                 PRIMARY KEY (emp_id)
            )

        .. seealso::

            :term:`composite primary key`

            `Primary key (via Wikipedia) <https://en.wikipedia.org/wiki/Primary_Key>`_

    composite primary key

        A :term:`primary key` that has more than one column. A particular database row is unique based on two or more columns rather than just a single value.

        .. seealso::

            :term:`primary key`

    foreign key constraint
        A referential constraint between two tables. A foreign key is a field or set of fields in a relational table that matches a :term:`candidate key` of another table. The foreign key can be used to cross-reference tables. (via Wikipedia)

        A foreign key constraint can be added to a table in standard SQL using :term:`DDL` like the following:

        .. sourcecode:: sql

            ALTER TABLE employee ADD CONSTRAINT dep_id_fk
            FOREIGN KEY (employee) REFERENCES department (dep_id)

        .. seealso::

            `Foreign Key Constraint (via Wikipedia) <https://en.wikipedia.org/wiki/Foreign_key_constraint>`_

    check constraint

        A check constraint is a condition that defines valid data when adding or updating an entry in a table of a relational database. A check constraint is applied to each row in the table.  (via Wikipedia)

        A check constraint can be added to a table in standard SQL using :term:`DDL` like the following:

        .. sourcecode:: sql

            ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5);

        .. seealso::

            `CHECK constraint (via Wikipedia) <https://en.wikipedia.org/wiki/Check_constraint>`_

    unique constraint
    unique key index
        A unique key index can uniquely identify each row of data values in a database table. A unique key index comprises a single column or a set of columns in a single database table. No two distinct rows or data records in a database table can have the same data value (or combination of data values) in those unique key index columns if NULL values are not used. Depending on its design, a database table may have many unique key indexes but at most one primary key index.

        (via Wikipedia)

        .. seealso::

            `Unique key (via Wikipedia) <https://en.wikipedia.org/wiki/Unique_key#Defining_unique_keys>`_

    transient
        This describes one of the major object states which an object can have within a :term:`Session`; a transient object is a new object that doesn't have any database identity and has not been associated with a session yet. When the object is added to the session, it moves to the :term:`pending` state.

        .. seealso::

            :ref:`session_object_states`

    pending
        This describes one of the major object states which an object can have within a :term:`Session`; a pending object is a new object that doesn't have any database identity, but has been recently associated with a session.  When the session emits a flush and the row is inserted, the object moves to the :term:`persistent` state.

        .. seealso::

            :ref:`session_object_states`

    deleted
        This describes one of the major object states which an object can have within a :term:`Session`; a deleted object is an object that was formerly persistent and has had a DELETE statement emitted to the database within a flush to delete its row. The object will move to the :term:`detached` state once the session's transaction is committed; alternatively, if the session's transaction is rolled back, the DELETE is reverted and the object moves back to the :term:`persistent` state.

        .. seealso::

            :ref:`session_object_states`

    persistent
        This describes one of the major object states which an object can have within a :term:`Session`; a persistent object is an object that has a database identity (i.e. a primary key) and is currently associated with a session. Any object that was previously :term:`pending` and has now been inserted is in the persistent state, as is any object that's been loaded by the session from the database. When a persistent object is removed from a session, it is known as :term:`detached`.

        .. seealso::

            :ref:`session_object_states`

    detached
        This describes one of the major object states which an object can have within a :term:`Session`; a detached object is an object that has a database identity (i.e. a primary key) but is not associated with any session.  An object that was previously :term:`persistent` and was removed from its session either because it was expunged, or the owning session was closed, moves into the detached state. The detached state is generally used when objects are being moved between sessions or when being moved to/from an external object cache.

        .. seealso::

            :ref:`session_object_states`

    attached
        Indicates an ORM object that is presently associated with a specific
        :term:`Session`.

        .. seealso::

            :ref:`session_object_states`

