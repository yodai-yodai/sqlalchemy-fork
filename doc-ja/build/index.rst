:orphan:

.. _index_toplevel:

========================
SQLAlchemy Documentation
========================

.. container:: left_right_container

  .. container:: leftmost

      .. rst-class:: h2

        Getting Started

  .. container::

    .. New to SQLAlchemy?   Start here:

    SQLAlchemyを初めてお使いの方は、ここから始めてください。

    .. * **For Python Beginners:** :ref:`Installation Guide <installation>` - basic guidance on installing with pip and similar

    * **For Python Beginners:** :ref:`Installation Guide <installation>` - pipなどを使用したインストールに関する基本的なガイダンス

    .. * **For Python Veterans:** :doc:`SQLAlchemy Overview <intro>` - brief architectural overview

    * **For Python Veterans:** :doc:`SQLAlchemy Overview <intro>` - アーキテクチャの簡単な概要

.. container:: left_right_container

  .. container:: leftmost

    .. rst-class:: h2

        Tutorials

  .. container::

    .. New users of SQLAlchemy, as well as veterans of older SQLAlchemy release series, should start with the :doc:`/tutorial/index`, which covers everything an Alchemist needs to know when using the ORM or just Core.

    SQLAlchemyの新しいユーザは、古いSQLAlchemyリリースシリーズのベテランと同様に、:doc:`/tutorial/index`から始める必要があります。これは、ORMまたは単にCoreを使用するときに錬金術師が知る必要のあるすべてをカバーしています。

    .. * **For a quick glance:** :doc:`/orm/quickstart` - a glimpse at what working with the ORM looks like

    * **For a quick glance:** :doc:`/orm/quickstart` - ORMを使った作業がどのようなものかを垣間見ることができます

    .. * **For all users:** :doc:`/tutorial/index` - In depth tutorial for Core and ORM

    * **For all users:** :doc:`/tutorial/index` - CoreとORMの詳細なチュートリアル


.. container:: left_right_container

  .. container:: leftmost

      .. rst-class:: h2

        Migration Notes

  .. container::

    .. Users coming from older versions of SQLAlchemy, especially those transitioning from the 1.x style of working, will want to review this documentation.

    古いバージョンのSQLAlchemyを使用しているユーザ、特に1.xスタイルから移行したユーザは、このドキュメントを読むとよいでしょう。

    .. * :doc:`Migrating to SQLAlchemy 2.0 <changelog/migration_20>` - Complete background on migrating from 1.3 or 1.4 to 2.0

    * :doc:`Migrating to SQLAlchemy 2.0 <changelog/migration_20>` - 1.3または1.4から2.0への移行の経緯

    .. * :doc:`What's New in SQLAlchemy 2.0? <changelog/whatsnew_20>` - New 2.0 features and behaviors beyond the 1.x migration

    * :doc:`What's New in SQLAlchemy 2.0? <changelog/whatsnew_20>` - 1.xへの移行後の2.0の新機能と動作

    .. * :doc:`Changelog catalog <changelog/index>` - Detailed changelogs for all SQLAlchemy Versions

    * :doc:`Changelog catalog <changelog/index>` - すべてのSQLAlchemyバージョンの詳細な変更ログ

.. container:: left_right_container

  .. container:: leftmost

      .. rst-class:: h2

      Reference and How To

  .. container:: orm

    .. **SQLAlchemy ORM** - Detailed guides and API reference for using the ORM

    **SQLAlchemy ORM** - ORMを使用するための詳細なガイドとAPIリファレンス

    .. * **Mapping Classes:**
    ..   :doc:`Mapping Python Classes <orm/mapper_config>` |
    ..   :doc:`Relationship Configuration <orm/relationships>`


    * **マッピングクラス:**
      :doc:`Mapping Python Classes <orm/mapper_config>` |
      :doc:`Relationship Configuration <orm/relationships>`

    .. * **Using the ORM:**
    ..   :doc:`Using the ORM Session <orm/session>` |
    ..   :doc:`ORM Querying Guide <orm/queryguide/index>` |
    ..   :doc:`Using AsyncIO <orm/extensions/asyncio>`

    * **ORMの使用:**
      :doc:`Using the ORM Session <orm/session>` |
      :doc:`ORM Querying Guide <orm/queryguide/index>` |
      :doc:`Using AsyncIO <orm/extensions/asyncio>`

    .. * **Configuration Extensions:**
    ..   :doc:`Association Proxy <orm/extensions/associationproxy>` |
    ..   :doc:`Hybrid Attributes <orm/extensions/hybrid>` |
    ..   :doc:`Mutable Scalars <orm/extensions/mutable>` |
    ..   :doc:`Automap <orm/extensions/automap>` |
    ..   :doc:`All extensions <orm/extensions/index>`

    * **構成の拡張:**
      :doc:`Association Proxy <orm/extensions/associationproxy>` |
      :doc:`Hybrid Attributes <orm/extensions/hybrid>` |
      :doc:`Mutable Scalars <orm/extensions/mutable>` |
      :doc:`Automap <orm/extensions/automap>` |
      :doc:`All extensions <orm/extensions/index>`

    .. * **Extending the ORM:**
    ..   :doc:`ORM Events and Internals <orm/extending>`

    * **ORMの拡張:**
      :doc:`ORM Events and Internals <orm/extending>`

    * **Other:**
      :doc:`Introduction to Examples <orm/examples>`

    * **その他:**
      :doc:`Introduction to Examples <orm/examples>`

  .. container:: core

    .. **SQLAlchemy Core** - Detailed guides and API reference for working with Core

    **SQLAlchemy Core** - Coreを操作するための詳細なガイドとAPIリファレンス

    .. * **Engines, Connections, Pools:**
    ..   :doc:`Engine Configuration <core/engines>` |
    ..   :doc:`Connections, Transactions, Results <core/connections>` |
    ..   :doc:`AsyncIO Support <orm/extensions/asyncio>` |
    ..   :doc:`Connection Pooling <core/pooling>`

    * **エンジン、接続、プール:**
      :doc:`Engine Configuration <core/engines>` |
      :doc:`Connections, Transactions, Results <core/connections>` |
      :doc:`AsyncIO Support <orm/extensions/asyncio>` |
      :doc:`Connection Pooling <core/pooling>`

    .. * **Schema Definition:**
    ..   :doc:`Overview <core/schema>` |
    ..   :ref:`Tables and Columns <metadata_describing_toplevel>` |
    ..   :ref:`Database Introspection (Reflection) <metadata_reflection_toplevel>` |
    ..   :ref:`Insert/Update Defaults <metadata_defaults_toplevel>` |
    ..   :ref:`Constraints and Indexes <metadata_constraints_toplevel>` |
    ..   :ref:`Using Data Definition Language (DDL) <metadata_ddl_toplevel>`

    * **スキーマ定義:**
      :doc:`Overview <core/schema>` |
      :ref:`Tables and Columns <metadata_describing_toplevel>` |
      :ref:`Database Introspection (Reflection) <metadata_reflection_toplevel>` |
      :ref:`Insert/Update Defaults <metadata_defaults_toplevel>` |
      :ref:`Constraints and Indexes <metadata_constraints_toplevel>` |
      :ref:`Using Data Definition Language (DDL) <metadata_ddl_toplevel>`

    .. * **SQL Statements:**
    ..   :doc:`SQL Expression Elements <core/sqlelement>` |
    ..   :doc:`Operator Reference <core/operators>` |
    ..   :doc:`SELECT and related constructs <core/selectable>` |
    ..   :doc:`INSERT, UPDATE, DELETE <core/dml>` |
    ..   :doc:`SQL Functions <core/functions>` |
    ..   :doc:`Table of Contents <core/expression_api>`

    * **SQL文:**
      :doc:`SQL Expression Elements <core/sqlelement>` |
      :doc:`Operator Reference <core/operators>` |
      :doc:`SELECT and related constructs <core/selectable>` |
      :doc:`INSERT, UPDATE, DELETE <core/dml>` |
      :doc:`SQL Functions <core/functions>` |
      :doc:`Table of Contents <core/expression_api>`

    .. * **Datatypes:**
    ..   :ref:`Overview <types_toplevel>` |
    ..   :ref:`Building Custom Types <types_custom>` |
    ..   :ref:`Type API Reference <types_api>`

    * **データ型:**
      :ref:`Overview <types_toplevel>` |
      :ref:`Building Custom Types <types_custom>` |
      :ref:`Type API Reference <types_api>`

    .. * **Core Basics:**
    ..   :doc:`Overview <core/api_basics>` |
    ..   :doc:`Runtime Inspection API <core/inspection>` |
    ..   :doc:`Event System <core/event>` |
    ..   :doc:`Core Event Interfaces <core/events>` |
    ..   :doc:`Creating Custom SQL Constructs <core/compiler>`

    * **コアの基本:**
      :doc:`Overview <core/api_basics>` |
      :doc:`Runtime Inspection API <core/inspection>` |
      :doc:`Event System <core/event>` |
      :doc:`Core Event Interfaces <core/events>` |
      :doc:`Creating Custom SQL Constructs <core/compiler>`

.. container:: left_right_container

    .. container:: leftmost

      .. rst-class:: h2

        Dialect Documentation

    .. container::

      .. The **dialect** is the system SQLAlchemy uses to communicate with various types of DBAPIs and databases.
      .. This section describes notes, options, and usage patterns regarding individual dialects.

      .. :doc:`PostgreSQL <dialects/postgresql>` |
      .. :doc:`MySQL and MariaDB <dialects/mysql>` |
      .. :doc:`SQLite <dialects/sqlite>` |
      .. :doc:`Oracle <dialects/oracle>` |
      .. :doc:`Microsoft SQL Server <dialects/mssql>`

      .. :doc:`More Dialects ... <dialects/index>`

    **ダイアレクト** は、SQLAlchemyがさまざまなタイプのDB APIやデータベースと通信するために使用するシステムです。このセクションでは、個々のダイアレクトに関する注意、オプション、および使用パターンについて説明します。
      :doc:`PostgreSQL <dialects/postgresql>` |
      :doc:`MySQL and MariaDB <dialects/mysql>` |
      :doc:`SQLite <dialects/sqlite>` |
      :doc:`Oracle <dialects/oracle>` |
      :doc:`Microsoft SQL Server <dialects/mssql>`

      :doc:`More Dialects ... <dialects/index>`

.. container:: left_right_container

  .. container:: leftmost

      .. rst-class:: h2

        Supplementary

  .. container::

    .. * :doc:`Frequently Asked Questions <faq/index>` - A collection of common problems and solutions
    .. * :doc:`Glossary <glossary>` - Terms used in SQLAlchemy's documentation
    .. * :doc:`Error Message Guide <errors>` - Explanations of many SQLAlchemy Errors
    .. * :doc:`Complete table of of contents <contents>`
    .. * :ref:`Index <genindex>`

    * :doc:`Frequently Asked Questions <faq/index>` - 一般的な問題と解決策の集合
    * :doc:`Glossary <glossary>` - SQLAlchemyのドキュメントで使用されている用語
    * :doc:`Error Message Guide <errors>` - 多くのSQLAlchemyエラーの説明
    * :doc:`Complete table of of contents <contents>`
    * :ref:`Index <genindex>`

