.. _overview_toplevel:
.. _overview:

========
Overview
========

.. The SQLAlchemy SQL Toolkit and Object Relational Mapper is a comprehensive set of tools for working with databases and Python. It has several distinct areas of functionality which can be used individually or combined together.
.. Its major components are illustrated below, with component dependencies organized into layers:

SQLAlchemy SQL Toolkit and Object Relational Mapperは、データベースとPythonを操作するための包括的なツール・セットです。これには、個別にまたは組み合わせて使用できるいくつかの異なる機能領域があります。その主要なコンポーネントを次に示します。コンポーネントの依存関係はレイヤーに編成されています。

.. image:: sqla_arch_small.png

.. Above, the two most significant front-facing portions of SQLAlchemy are the **Object Relational Mapper (ORM)** and the **Core**.

上の図で、SQLAlchemyの前面にある最も重要な2つの部分は、 **Object Relational Mapper(ORM)** と **Core** です。

.. Core contains the breadth of SQLAlchemy's SQL and database integration and description services, the most prominent part of this being the **SQL Expression Language**.

Coreには、SQLAlchemyのSQLとデータベースの統合および記述サービスの幅広さが含まれており、その中で最も顕著な部分は **SQL式言語** です。

.. The SQL Expression Language is a toolkit on its own, independent of the ORM package, which provides a system of constructing SQL expressions represented by composable objects, which can then be "executed" against a target database within the scope of a specific transaction, returning a result set.
.. Inserts, updates and deletes (i.e. :term:`DML`) are achieved by passing SQL expression objects representing these statements along with dictionaries that represent parameters to be used with each statement.

SQL式言語は、ORMパッケージとは独立した独自のツールキットであり、構成可能なオブジェクトによって表されるSQL式を構築するシステムを提供し、特定のトランザクションのスコープ内でターゲットデータベースに対して"実行"し、結果セットを返すことができます。挿入、更新、削除(すなわち :term:`DML`)は、これらの文を表すSQL式オブジェクトと、各文で使用されるパラメータを表す辞書を渡すことによって実現されます。

.. The ORM builds upon Core to provide a means of working with a domain object model mapped to a database schema.
.. When using the ORM, SQL statements are constructed in mostly the same way as when using Core, however the task of DML, which here refers to the persistence of business objects in a database, is automated using a pattern called :term:`unit of work`, which translates changes in state against mutable objects into INSERT, UPDATE and DELETE constructs which are then invoked in terms of those objects.
.. SELECT statements are also augmented by ORM-specific automations and object-centric querying capabilities.

ORMはCore上に構築され、データベーススキーマにマップされたドメインオブジェクトモデルを操作する手段を提供します。ORMを使用する場合、SQL文はCoreを使用する場合とほぼ同じ方法で構築されますが、DMLのタスク(ここではデータベース内のビジネスオブジェクトの永続性を指します)は、 :term:`unit of work` と呼ばれるパターンを使用して自動化されます。このパターンは、可変オブジェクトに対する状態の変更をINSERT、UPDATE、およびDELETE構文に変換し、これらのオブジェクトに関して呼び出されます。SELECT文は、ORM固有の自動化とオブジェクト中心のクエリ機能によっても強化されます。

.. Whereas working with Core and the SQL Expression language presents a schema-centric view of the database, along with a programming paradigm that is oriented around immutability, the ORM builds on top of this a domain-centric view of the database with a programming paradigm that is more explicitly object-oriented and reliant upon mutability.
.. Since a relational database is itself a mutable service, the difference is that Core/SQL Expression language is command oriented whereas the ORM is state oriented.

CoreとSQL式言語を使用すると、不変性を中心としたプログラミングパラダイムとともに、データベースのスキーマ中心のビューが表示されるのに対して、ORMは、この上に、より明示的にオブジェクト指向であり、可変性に依存するプログラミングパラダイムを使用して、データベースのドメイン中心のビューを構築します。リレーショナル・データベース自体が可変サービスであるため、Core/SQL式言語がコマンド指向であるのに対して、ORMは状態指向である点が異なります。

.. _doc_overview:

Documentation Overview
======================

The documentation is separated into four sections:

.. * :ref:`unified_tutorial` - this all-new tutorial for the 1.4/2.0 series of SQLAlchemy introduces the entire library holistically, starting from a   description of Core and working more and more towards ORM-specific concepts. New users, as well as users coming from the 1.x series of   SQLAlchemy, should start here.

* :ref:`unified_tutorial` - SQLAlchemyの1.4/2.0シリーズのためのこの全く新しいチュートリアルでは、Coreの説明から始まり、ORM固有の概念に向けてますます作業を進めながら、ライブラリ全体を総合的に紹介しています。SQLAlchemyの1.xシリーズのユーザーだけでなく、新規ユーザーもここから始める必要があります。

.. * :ref:`orm_toplevel` -  In this section, reference documentation for the ORM is presented.

* :ref:`orm_toplevel` - このセクションでは、ORMの参考資料を紹介します。

.. * :ref:`core_toplevel` - Here, reference documentation for everything else within Core is presented. SQLAlchemy engine, connection, and pooling services are also described here.

* :ref:`core_toplevel` - ここでは、Core内のその他すべての参照ドキュメントを示します。SQLAlchemyエンジン、接続、プーリング・サービスについてもここで説明します。

.. * :ref:`dialect_toplevel` - Provides reference documentation for all :term:`dialect` implementations, including :term:`DBAPI` specifics.

* :ref:`dialect_toplevel` - :term:`DBAPI` 仕様を含む、すべての :term:`dialect` 実装のリファレンスドキュメントを提供します。

Code Examples
=============

.. Working code examples, mostly regarding the ORM, are included in the SQLAlchemy distribution. A description of all the included example applications is at :ref:`examples_toplevel`.

SQLAlchemyディストリビューションには、主にORMに関する実用的なコード例が含まれています。含まれているすべてのサンプルアプリケーションの説明は :ref:`examples_toplevel` にあります。

.. There is also a wide variety of examples involving both core SQLAlchemy constructs as well as the ORM on the wiki.
.. See `Theatrum Chemicum <https://www.sqlalchemy.org/trac/wiki/UsageRecipes>`_.

wikiには、コアのSQLAlchemy構成体とORMの両方を含むさまざまな例もあります。 `Theatrum Chemicum <https://www.sqlalchemy.org/trac/wiki/UsageRecipes>`_ を参照してください。

.. _installation:

Installation Guide
==================

Supported Platforms
-------------------

.. SQLAlchemy supports the following platforms:

SQLAlchemyは次のプラットフォームをサポートしています。

.. * cPython 3.7 and higher
.. * Python-3 compatible versions of `PyPy <http://pypy.org/>`_

* cPython 3.7以上
* Python 3互換バージョンの`PyPy<http://PyPy.org/>`_

.. versionchanged:: 2.0

  ..  SQLAlchemy now targets Python 3.7 and above.

  SQLAlchemyはPython 3.7以降に対応しました。

AsyncIO Support
----------------

.. SQLAlchemy's ``asyncio`` support depends upon the `greenlet <https://pypi.org/project/greenlet/>`_ project.
.. This dependency will be installed by default on common machine platforms, however is not supported on every architecture and also may not install by default on less common architectures. See the section :ref:`asyncio_install` for additional details on ensuring asyncio support is present.

SQLAlchemyの"`asyncio`"サポートは、 `greenlet <https://pypi.org/project/greenlet/>`_ プロジェクトに依存しています。 この依存関係は一般的なマシンプラットフォームにデフォルトでインストールされますが、すべてのアーキテクチャでサポートされているわけではなく、あまり一般的でないアーキテクチャにもデフォルトでインストールされない場合があります。asyncioサポートが存在することを確認するための詳細については、 :ref:`asyncio_install` を参照してください。

Supported Installation Methods
-------------------------------

.. SQLAlchemy installation is via standard Python methodologies that are based on `setuptools <https://pypi.org/project/setuptools/>`_, either by referring to ``setup.py`` directly or by using `pip <https://pypi.org/project/pip/>`_ or other setuptools-compatible approaches.

SQLAlchemyのインストールは、 `setuptools <https://pypi.org/project/setuptools/>`_ に基づく標準的なPythonの方法で行われます。これは、 ``setup.py`` を直接参照するか、 `pip <https://pypi.org/project/pip/>`_ やその他のsetuptools互換の方法を使用します。

Install via pip
---------------

.. When ``pip`` is available, the distribution can be downloaded from PyPI and installed in one step:

``pip`` が利用可能な場合は、ディストリビューションをPyPIからダウンロードして、1ステップでインストールできます。

.. sourcecode:: text

    pip install SQLAlchemy

.. This command will download the latest **released** version of SQLAlchemy from the `Python Cheese Shop <https://pypi.org/project/SQLAlchemy>`_ and install it to your system. For most common platforms, a Python Wheel file will be downloaded which provides native Cython / C extensions prebuilt.

このコマンドは、`Python Cheese Shop <https://pypi.org/project/SQLAlchemy>`_ から最新の **リリースされた** バージョンのSQLAlchemyをダウンロードし、システムにインストールします。ほとんどの一般的なプラットフォームでは、ネイティブの Cython / C 拡張機能が事前に構築されたPython Wheelファイルがダウンロードされます。

.. In order to install the latest **prerelease** version, such as ``2.0.0b1``, pip requires that the ``--pre`` flag be used:

``2.0.0b1`` のような最新の **プレリリース** バージョンをインストールするには、pipは ``--pre`` フラグを使用する必要があります。

.. sourcecode:: text

    pip install --pre SQLAlchemy

.. Where above, if the most recent version is a prerelease, it will be installed instead of the latest released version.

上記の場合、最新バージョンがプレリリースであれば、最新リリースバージョンではなくプレリリースバージョンがインストールされます。

Installing manually from the source distribution
-------------------------------------------------

.. When not installing from pip, the source distribution may be installed using the ``setup.py`` script:

pipからインストールしない場合、ソースディストリビューションは ``setup.py`` スクリプトを使ってインストールできます。

.. sourcecode:: text

    python setup.py install

.. The source install is platform agnostic and will install on any platform regardless of whether or not Cython / C build tools are installed. As the next section :ref:`c_extensions` details, ``setup.py`` will attempt to build using Cython / C if possible but will fall back to a pure Python installation otherwise.

ソースインストールはプラットフォームに依存せず、Cython / C ビルドツールがインストールされているかどうかにかかわらず、どのプラットフォームにもインストールされます。次のセクション :ref:`c_extensions` で詳しく説明しますが、 ``setup.py`` は可能であれば Cython / C を使ってビルドしようとしますが、そうでなければ純粋なPythonインストールに戻ります。

.. _c_extensions:

Building the Cython Extensions
----------------------------------

.. SQLAlchemy includes Cython_ extensions which provide an extra speed boost within various areas, with a current emphasis on the speed of Core result sets.

SQLAlchemyには Cython_ extensionsが含まれており、さまざまな領域で速度をさらに向上させることができます。現在はコア結果セットの速度に重点が置かれています。

.. versionchanged:: 2.0  SQLAlchemy C拡張はCythonを使用して書き直されました。

.. ``setup.py`` will automatically build the extensions if an appropriate platform is detected, assuming the Cython package is installed. A complete manual build looks like:

``setup.py`` は、Cythonパッケージがインストールされていれば、適切なプラットフォームが検出されれば自動的に拡張機能をビルドします。完全な手動ビルドは次のようになります。

.. sourcecode:: text

    # cd into SQLAlchemy source distribution
    cd path/to/sqlalchemy

    # install cython
    pip install cython

    # optionally build Cython extensions ahead of install
    python setup.py build_ext

    # run the install
    python setup.py install

.. Source builds may also be performed using :pep:`517` techniques, such as using build_:

ソースの構築は、build_ のような :pep:`517` のテクニックを使って行うこともできます。

.. sourcecode:: text

    # cd into SQLAlchemy source distribution
    cd path/to/sqlalchemy

    # install build
    pip install build

    # build source / wheel dists
    python -m build

.. If the build of the Cython extensions fails due to Cython not being installed, a missing compiler or other issue, the setup process will output a warning message and re-run the build without the Cython extensions upon completion, reporting final status.

Cythonがインストールされていない、コンパイラが見つからない、またはその他の問題が原因でCython拡張機能のビルドが失敗した場合、セットアッププロセスは警告メッセージを出力し、完了時にCython拡張機能なしでビルドを再実行し、最終ステータスを報告します。

.. To run the build/install without even attempting to compile the Cython extensions, the ``DISABLE_SQLALCHEMY_CEXT`` environment variable may be specified. The use case for this is either for special testing circumstances, or in the rare case of compatibility/build issues not overcome by the usual "rebuild" mechanism:

Cython拡張モジュールをコンパイルすることもせずにビルド/インストールを実行するには、 ``DISABLE_SQLALCHEMY_CEXT`` 環境変数を指定します。このユースケースは、特別なテスト状況の場合、または通常の"再構築"メカニズムでは克服できない互換性/ビルドの問題のまれなケースのいずれかです。

.. sourcecode:: text

  export DISABLE_SQLALCHEMY_CEXT=1; python setup.py install


.. _Cython: https://cython.org/

.. _build: https://pypi.org/project/build/


Installing a Database API
----------------------------------

.. SQLAlchemy is designed to operate with a :term:`DBAPI` implementation built for a particular database, and includes support for the most popular databases.
.. The individual database sections in :doc:`/dialects/index` enumerate the available DBAPIs for each database, including external links.

SQLAlchemyは、特定のデータベース用に構築された :term:`DBAPI` 実装で動作するように設計されており、最も一般的なデータベースをサポートしています。
:doc:`/dialects/index` の個々のデータベースセクションには、外部リンクを含め、各データベースで利用可能なDB APIが列挙されています。



Checking the Installed SQLAlchemy Version
------------------------------------------

.. This documentation covers SQLAlchemy version 2.0. If you're working on a system that already has SQLAlchemy installed, check the version from your Python prompt like this::

このドキュメントでは、SQLAlchemyバージョン2.0について説明します。すでにSQLAlchemyがインストールされているシステムで作業している場合は、次のようにPythonプロンプトからバージョンを確認してください::

     >>> import sqlalchemy
     >>> sqlalchemy.__version__  # doctest: +SKIP
     2.0.0

Next Steps
----------

.. With SQLAlchemy installed, new and old users alike can :ref:`Proceed to the SQLAlchemy Tutorial <unified_tutorial>`.

SQLAlchemyがインストールされていれば、今までと同じように :ref:`Proceed to the SQLAlchemy Tutorial <unified_tutorial>` で学習できます。

.. _migration:

1.x to 2.0 Migration
=====================

.. Notes on the new API released in SQLAlchemy 2.0 is available here at :doc:`changelog/migration_20`.

SQLAlchemy 2.0でリリースされた新しいAPIに関する注記は、 :doc:`changelog/migration_20` を参照してください。
